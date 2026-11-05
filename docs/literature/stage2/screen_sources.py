from pathlib import Path
import re,json
import unicodedata
def norm(doi):
    return (doi or '').lower().removeprefix('https://doi.org/')
def add(d, title, doi, source, year=None):
    key=norm(doi) or 'title:'+re.sub(r'\W+','',unicodedata.normalize('NFKC',title.lower()))
    r=d.setdefault(key,{'title':title,'doi':norm(doi),'sources':[],'year':year})
    if source not in r['sources']: r['sources'].append(source)
def gather():
    p=Path(__file__).resolve().parent/'evidence'; d={}
    original = sorted(list(p.glob('Q*.json'))+list(p.glob('*_citing.json'))+list(p.glob('*_refs*.json')))
    for f in original + sorted(p.glob('A1?.json')):
        j=json.loads(f.read_bytes()); rows=j['results'] if 'results' in j else j['message']['items']
        for x in rows:
            title=x.get('display_name') or x['title'][0]
            add(d,title,x.get('doi') or x.get('DOI'),f.stem,x.get('publication_year') or x.get('published',{}).get('date-parts',[[None]])[0][0])
    return d
if __name__=='__main__':
    for i,(k,r) in enumerate(gather().items(),1): print(f'{i}: {r["title"]}')
