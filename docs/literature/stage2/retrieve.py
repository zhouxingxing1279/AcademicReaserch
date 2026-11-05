"""Collect a dated bibliography snapshot. Reuse cached bodies; never replace a search round."""
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
OUT = BASE / 'evidence'
OUT.mkdir(exist_ok=True)
CR = 'https://api.crossref.org/works'
OA = 'https://api.openalex.org/works'
CUTOFF = '2026-11-05'
QUERIES = [line.split('|')[2].strip() for line in (BASE / 'search_protocol.md').read_text(encoding='utf8').splitlines() if line.startswith(('| 应用 |','| 基础 |','| 方法迁移 |','| 前沿 |'))]
OA_FIELDS = 'id,doi,display_name,publication_year,publication_date,open_access,locations,referenced_works'
CR_FIELDS = 'DOI,title,published,author,container-title,type'
def read_job(job):
    key, url = job
    if not re.fullmatch(r'[A-Za-z0-9_]+', key):
        raise ValueError(f'Invalid snapshot key: {key}')
    body = OUT / (key + '.json')
    if body.exists():
        data = body.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        previous = log.get(key, {})
        if previous.get('url') != url or previous.get('sha256') != digest:
            raise ValueError(f'Existing snapshot has a different URL or digest: {key}')
        return key, url, 200, digest, json.loads(data)
    try:
        req = Request(url, headers={'User-Agent':'AcademicResearch-BibliographicAudit/1.0','Accept':'application/json'})
        with urlopen(req, timeout=18) as r:
            data = r.read()
            status = r.status
        obj = json.loads(data)
        if status == 200:
            body.write_bytes(data)
        return key, url, status, hashlib.sha256(data).hexdigest(), obj
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as e:
        return key, url, getattr(e,'code',None), None, {'error':str(e)}

def run(jobs):
    for key,url,status,sha,obj in map(read_job, jobs):
        old = log.get(key, {})
        history = old.get('prior_failures', [])
        if old and not old.get('sha256'):
            history = history + [{'status':old.get('status'),'error':old.get('error')}]
        log[key] = {'url':url,'status':status,'file':'evidence/'+key+'.json' if sha else None,'sha256':sha,'prior_failures':history}
        if not sha:
            log[key]['error']=obj['error']
        print(key,status,flush=True)

def query(base, **kw):
    return base+'?'+urlencode(kw)

logfile = BASE / 'retrieval_log.json'
log = json.loads(logfile.read_text(encoding='utf8')) if logfile.exists() else {}
seeds = [(parts[1].strip(),parts[3].strip()) for line in (BASE.parents[1]/'research/research_background.md').read_text(encoding='utf8').splitlines() if re.match(r'^\| [DMF]\d+ \|',line) for parts in [line.split('|')]]
if len(sys.argv)>1:
    run([(key, CR+'/'+quote(doi,safe='/')) for key,doi in (arg.split('=',1) for arg in sys.argv[1:])])
else:
    jobs=[]
    for i,q in enumerate(QUERIES,1):
        since = ',from-pub-date:2024-01-01' if i>=8 else ''
        jobs.append((f'Q{i}_CR',query(CR,**{'query.bibliographic':q,'rows':10,'select':CR_FIELDS,'filter':'until-pub-date:'+CUTOFF+since})))
        since = ',from_publication_date:2024-01-01' if i>=8 else ''
        jobs.append((f'Q{i}_OA',query(OA,search=q,per_page=10,select=OA_FIELDS,filter='to_publication_date:'+CUTOFF+since)))
    jobs.extend((key,CR+'/'+quote(doi,safe='/')) for key,doi in seeds)
    jobs.extend((key+'_OA',OA+'/https://doi.org/'+doi) for key,doi in seeds if key in ('M1','M2','D4'))
    run(jobs)
    for key in ('M1','M2'):
        p=OUT/(key+'_OA.json')
        if not p.exists():
            continue
        rec=json.loads(p.read_bytes())
        ids=[x.split('/')[-1] for x in rec.get('referenced_works',[])]
        batch=[(key+'_citing',query(OA,filter='cites:'+rec['id'].split('/')[-1]+',to_publication_date:'+CUTOFF,per_page=100,select=OA_FIELDS))]
        for start in range(0,len(ids),40):
            batch.append((key+f'_refs{start}',query(OA,filter='openalex:'+'|'.join(ids[start:start+40]),per_page=40,select=OA_FIELDS)))
        run(batch)
logfile.write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
