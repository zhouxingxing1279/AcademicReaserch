"""Dispatch isolated CLI review conversations, or materialize prompts with --prepare-only."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent


def utc():
    return datetime.now(timezone.utc).isoformat()


def prompt_for(role, task, contract):
    return (
        f"你是本轮 {role} 独立研究员；仅按下文冻结合同单独工作。不要读取其他组、以往聊天、用户目录或仓库。"
        "允许在当前目录做只读计算，数据如需接口不可用就给手算见证。不要派生其他代理，不修改文件。"
        "直接用中文提交一份自足研究备忘录（建议 500–1000 字），区分已证/数值/猜想，给出可被推翻的结论、最强基线与局限。"
        f"没有来源时不声称查新。不要向用户提问。专项委托：{task}\n\n{contract}"
    )


def worker(role, task, contract, root, executable, prepare):
    directory = root / role
    directory.mkdir()
    prompt = prompt_for(role, task, contract).encode("utf-8")
    (directory / "prompt.txt").write_bytes(prompt)
    info = {
        "role": role,
        "prompt_sha256": sha256(prompt).hexdigest(),
        "started_at": utc(),
        "status": "prepared",
    }
    if prepare:
        return info
    out = directory / "result.md"
    try:
        run = subprocess.run(
            [
                executable,
                "--ask-for-approval",
                "never",
                "exec",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "-C",
                str(directory),
                "--color",
                "never",
                "--json",
                "-o",
                str(out),
                "-",
            ],
            cwd=directory,
            input=prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1200,
            check=False,
        )
        info["exit_code"] = run.returncode
        events = []
        for line in run.stdout.decode("utf-8", errors="replace").splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        info["thread_ids"] = [e["thread_id"] for e in events if e.get("type") == "thread.started"]
        completed = any(e.get("type") == "turn.completed" for e in events)
        if run.returncode == 0 and completed and out.is_file() and out.stat().st_size:
            info.update(status="completed", report_sha256=sha256(out.read_bytes()).hexdigest())
        else:
            # The CLI's error stream can contain private service URLs.
            diagnostic = (run.stdout + run.stderr).lower()
            info["status"] = "failed"
            info["reason"] = (
                "service_license_expired"
                if b"license has expired" in diagnostic
                else "rate_limited"
                if b"429" in diagnostic
                else "cli_or_missing_result"
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        info.update(status="failed", reason=type(exc).__name__)
    info["ended_at"] = utc()
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="a NEW directory for this run")
    parser.add_argument(
        "--prepare-only", action="store_true", help="write prompts without invoking Codex"
    )
    parser.add_argument(
        "--role", choices=("baseline", "candidate", "adversary"), help="run one role"
    )
    args = parser.parse_args()
    root = args.output.resolve()
    executable = shutil.which("codex")
    if not args.prepare_only and executable is None:
        parser.error("Codex CLI is required")
    root.mkdir(parents=True, exist_ok=False)
    roles = json.loads((HERE / "roles.json").read_text(encoding="utf-8"))
    frozen = (HERE / "CONTRACT.md").read_bytes()
    contract = frozen.decode("utf-8").replace("\r\n", "\n")
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(worker, role, task, contract, root, executable, args.prepare_only)
            for role, task in roles.items()
            if args.role is None or role == args.role
        ]
        attempts = [f.result() for f in futures]
    manifest = {"contract_sha256": sha256(frozen).hexdigest(), "attempts": attempts}
    (root / "run.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for a in attempts:
        print(a["role"], a["status"])
    return int(any(a["status"] == "failed" for a in attempts))


if __name__ == "__main__":
    raise SystemExit(main())
