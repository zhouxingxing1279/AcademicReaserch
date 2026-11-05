"""按 DOI 下载单篇 IEEE 论文（Windows + Chrome）。

示例：python scripts/download_ieee.py 10.1109/TAC.2018.2791899
需要 PATH 中的 pdfinfo 和 pdftotext。先尝试直连，必要时由 Chrome 使用已有机构会话。
要自动落盘，可在 chrome://settings/content/pdfDocuments 选择“下载 PDF”，
并在 Chrome 下载设置中关闭“下载前询问每个文件的保存位置”。
若 Chrome 自定义了下载目录，请通过 --downloads 指定。
"""
import argparse
from http.client import HTTPException
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "docs/literature/sources/ieee_local"
AGENT = "AcademicReaserch-IEEE/1.0"


def ieee_doi(value):
    value = value.strip()
    if value.lower().startswith(("https://doi.org/", "http://doi.org/")):
        value = unquote(urlsplit(value).path.lstrip("/"))
    if not re.fullmatch(r"10\.1109/[A-Za-z0-9._();:/-]+", value, re.I):
        raise ValueError("请输入完整的 IEEE DOI（10.1109/...）或对应的 doi.org 链接。")
    return value.lower()


def article_metadata(doi):
    req = Request("https://api.crossref.org/works/" + quote(doi, safe="/"),
                  headers={"User-Agent": AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=20) as response:
        record = json.load(response)["message"]
    if record["DOI"].lower() != doi:
        raise ValueError("Crossref 返回的 DOI 与请求不符。")
    titles = record.get("title", [])
    title = titles[0] if titles else ""
    urls = [record.get("resource", {}).get("primary", {}).get("URL", "")]
    urls.extend(item.get("URL", "") for item in record.get("link", []))
    for url in urls:
        parts = urlsplit(url)
        if not (parts.hostname or "").endswith(".ieee.org"):
            continue
        number = parse_qs(parts.query).get("arnumber", [""])[0]
        if re.fullmatch(r"[0-9]+", number):
            return number, title
        match = re.fullmatch(r"/(?:abstract/)?document/([0-9]+)/?", parts.path)
        if match:
            return match[1], title
    raise ValueError("Crossref 没有提供 IEEE 文献号；请用 --article-number 指定论文页中的数字。")


def fetch_pdf(url, dest):
    req = Request(url, headers={"User-Agent": AGENT, "Accept": "application/pdf"})
    with urlopen(req, timeout=25) as response:
        prefix = response.read(8)
        if response.status != 200 or not prefix.startswith(b"%PDF-"):
            raise ValueError(f"IEEE 返回 HTTP {response.status}，未取得 PDF。")
        with dest.open("wb") as out:
            out.write(prefix)
            shutil.copyfileobj(response, out)


def pdf_pages(path, doi):
    with path.open("rb") as stream:
        if not stream.read(8).startswith(b"%PDF-"):
            raise ValueError("文件头不是 PDF。")
        stream.seek(max(0, path.stat().st_size - 2048))
        if b"%%EOF" not in stream.read():
            raise ValueError("PDF 尚未完整写入。")
    info = subprocess.check_output(["pdfinfo", str(path)], stderr=subprocess.DEVNULL, timeout=20)
    pages = re.search(rb"(?m)^Pages:\s+([1-9]\d*)\s*$", info)
    if not pages:
        raise ValueError("无法核对 PDF 页数。")
    front = subprocess.check_output(
        ["pdftotext", "-f", "1", "-l", "2", "-enc", "UTF-8", str(path), "-"],
        stderr=subprocess.DEVNULL, timeout=20,
    ).decode("utf-8").lower()
    if not re.search(re.escape(doi) + r"(?![a-z0-9._/-]*[a-z0-9])", front):
        raise ValueError("首页及次页未识别出请求的 DOI，文件未归档。")
    return int(pages[1])


def downloads_folder():
    if sys.platform == "win32":
        import winreg
        try:
            key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg:
                value = winreg.QueryValueEx(reg, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
            return Path(os.path.expandvars(value))
        except OSError:
            pass
    return Path.home() / "Downloads"


def chrome_executable():
    for var in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        if os.environ.get(var):
            exe = Path(os.environ[var]) / "Google/Chrome/Application/chrome.exe"
            if exe.is_file():
                return str(exe)
    exe = shutil.which("google-chrome") or shutil.which("chrome")
    if not exe:
        raise ValueError("找不到 Chrome；可以用 --direct-only 仅尝试直连。")
    return exe


def snapshot(folder):
    files = {}
    for path in folder.iterdir():
        if path.suffix.lower() not in (".pdf", ".jsp"):
            continue
        try:
            stat = path.stat()
            if path.is_file():
                files[path] = (stat.st_mtime_ns, stat.st_size)
        except FileNotFoundError:
            continue
    return files


def browser_pdf(url, doi, folder, timeout, temp, number, title):
    if not folder.is_dir():
        raise ValueError(f"下载目录不存在：{folder}。请用 --downloads 指定 Chrome 的下载目录。")
    seen = snapshot(folder)
    # A preview can be saved after a previous run has timed out. Reuse only
    # plausible filenames, and still verify the DOI in the copied document.
    title_key = re.sub(r"[\W_]", "", title.casefold())
    for path in seen:
        name_key = re.sub(r"[\W_]", "", path.stem.casefold())
        if number not in path.stem and not (title_key and title_key in name_key):
            continue
        try:
            shutil.copyfile(path, temp)
            return pdf_pages(temp, doi)
        except (OSError, ValueError, subprocess.SubprocessError):
            continue
    print(f"正在用 Chrome 打开 IEEE 官方 PDF，等候文件写入 {folder}", flush=True)
    print("若 Chrome 显示预览，请点下载图标；若显示机构登录页，请在 Chrome 完成登录。", flush=True)
    subprocess.Popen([chrome_executable(), url])
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        for path, stamp in snapshot(folder).items():
            if seen.get(path) == stamp:
                continue
            try:
                shutil.copyfile(path, temp)
                pages = pdf_pages(temp, doi)
            except OSError:
                continue  # A new file can be locked or renamed during the scan.
            except (ValueError, subprocess.SubprocessError):
                seen[path] = stamp  # Retry when the file changes.
                continue
            return pages
        time.sleep(0.7)
    raise ValueError(f"等候超时，未在 {folder} 收到包含目标 DOI 的完整 PDF。"
                     f"请核对下载目录和论文访问权限：https://ieeexplore.ieee.org/document/{number}/")


def download(args):
    doi = ieee_doi(args.doi)
    for tool in ("pdfinfo", "pdftotext"):
        if not shutil.which(tool):
            raise ValueError(f"缺少 {tool}；请先将 Poppler 的 bin 目录加入 PATH。")
    out = args.out.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    prefix, suffix = doi.split("/", 1)
    target = out / (prefix + "_" + quote(suffix, safe="") + ".pdf")
    if target.exists():
        pages = pdf_pages(target, doi)
        print(f"已有已核对文件（{pages} 页）：{target}")
        return
    number, title = (args.article_number, "") if args.article_number else article_metadata(doi)
    if not re.fullmatch(r"[0-9]+", number):
        raise ValueError("IEEE 文献号必须是纯数字。")
    url = f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={number}"
    # Stage on the output volume and publish without replacing an existing paper.
    with tempfile.TemporaryDirectory(prefix=".ieee-", dir=out) as work:
        temp = Path(work) / "paper.part"
        try:
            fetch_pdf(url, temp)
            pages = pdf_pages(temp, doi)
        except (ValueError, HTTPError, URLError, HTTPException, TimeoutError, subprocess.SubprocessError) as error:
            print(f"直连：{error}", file=sys.stderr, flush=True)
            if args.direct_only:
                raise ValueError("仅直连模式已结束。") from error
            pages = browser_pdf(url, doi, args.downloads.expanduser().resolve(), args.wait, temp, number, title)
        try:
            if os.name == "nt":
                os.rename(temp, target)  # On Windows, fails if the destination exists.
            else:
                os.link(temp, target)
        except FileExistsError:
            pages = pdf_pages(target, doi)
    print(f"已核对 DOI {doi}，共 {pages} 页。文件：{target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("doi", help="IEEE DOI 或 doi.org 链接")
    parser.add_argument("--article-number", help="可选，IEEE 文献号；指定后免查 Crossref")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="归档目录")
    parser.add_argument("--downloads", type=Path, default=downloads_folder(), help="Chrome 实际下载目录")
    parser.add_argument("--wait", type=int, default=120, help="等候浏览器下载的秒数（默认 120）")
    parser.add_argument("--direct-only", action="store_true", help="仅直连；不打开浏览器")
    options = parser.parse_args()
    if options.wait <= 0:
        parser.error("--wait 必须为正数")
    try:
        download(options)
    except (OSError, HTTPException, ValueError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"{exc}\n")
