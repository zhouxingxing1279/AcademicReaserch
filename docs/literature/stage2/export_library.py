"""Rebuild the BibTeX, comparison table, and reading cards from database.json."""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABELS = {
    'problem': '研究问题', 'model': '动力学模型', 'state_dimension': '状态维度',
    'control_input': '控制输入', 'estimator': '状态估计', 'uncertainty': '不确定性与量测',
    'mpc': 'MPC 结构', 'guarantee': '理论保证', 'experiment': '仿真与实验',
    'limitations': '局限与待核', 'relation': '与本课题的关系'
}

def tex(text):
    return str(text).replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')

def format_bib(record):
    types = {'journal-article': 'article', 'proceedings-article': 'inproceedings', 'preprint': 'misc'}
    kind = types[record['type']]
    author = ' and '.join(a['family'] + ', ' + a['given'] for a in record['authors'])
    fields = {'author': tex(author), 'title': '{' + tex(record['title']) + '}', 'year': record['year']}
    if kind == 'misc':
        fields.update(eprint='2105.03427', archivePrefix='arXiv')
    else:
        fields['journal' if kind=='article' else 'booktitle'] = tex(record['venue'])
        fields.update(volume=record['volume'], number=record['issue'], pages=record['pages'].replace('-', '--'))
    fields.update(doi=record['doi'], url=record['publication_url'])
    items = [f'  {k} = {{{v}}}' for k,v in fields.items() if v]
    return '@' + kind + '{' + record['citekey'] + ',\n' + ',\n'.join(items) + '\n}'

def render(book):
    records = book['records']
    if list(LABELS) != book['extraction_fields']:
        raise ValueError('extraction schema differs from export schema')
    bib = '\n\n'.join(format_bib(r) for r in records) + '\n'
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['ID','citekey','题名','出版年','DOI','证据层级','原文/记录','定位',*LABELS.values()])
    cards = ['# 阶段 2 逐篇阅读卡', '', '每张卡的依据见“定位”。理论承诺与本文对本课题的解释分栏保存。完整元数据及持久编号见[主库](database.json)。', '']
    for r in records:
        writer.writerow([r[key] for key in ('id','citekey','title','year','doi','level','source','locator',*LABELS)])
        cards.extend([f"## {r['id']} · {r['title']}", '',
                      f"{', '.join(a['given']+' '+a['family'] for a in r['authors'])}，{r['year']}，{r['venue']}。[出版或预印本记录](https://doi.org/{r['doi']})", '',
                      f"**{r['level']}**　{r['locator']}。[来源]({r['source']})", '',
                      '| 提取项 | 本文证据 |','|---|---|'])
        cards.extend(f'| {label} | {r[key]} |' for key,label in LABELS.items())
        cards.append('')
        if r['version_notes']:
            cards.extend([r['version_notes'], ''])
    return {'references.bib': bib.encode('utf8'), 'comparison.csv': stream.getvalue().encode('utf-8-sig'),
            'reading_cards.md': ('\n'.join(cards).rstrip() + '\n').encode('utf8')}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    book = json.loads((ROOT/'database.json').read_bytes())
    for name, data in render(book).items():
        path = ROOT/name
        if args.check:
            if path.read_bytes() != data:
                raise SystemExit(f'Export differs: {name}')
        else:
            path.write_bytes(data)
    print(f"{len(book['records'])} records; three exports {'verified' if args.check else 'written'}.")

if __name__=='__main__':
    main()
