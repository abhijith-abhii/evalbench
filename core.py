from pathlib import Path
from collections import Counter
import json,re,numpy as np
ROOT=Path(__file__).parent

def tokens(text):return re.findall(r'\w+',text.lower())
def score(answer,expected):
 a,b=tokens(answer),tokens(expected);overlap=sum((Counter(a)&Counter(b)).values());precision=overlap/len(a) if a else 0;recall=overlap/len(b) if b else 0
 return {'exact_match':int(a==b),'token_f1':2*precision*recall/(precision+recall) if precision+recall else 0}
def compare(cases,left,right):
 ids=[c['id'] for c in cases]
 if len(set(ids))!=len(ids):raise ValueError('Duplicate case IDs')
 if set(left)!=set(ids) or set(right)!=set(ids):raise ValueError('Both runs must cover exactly the same case IDs')
 rows=[]
 for c in cases:
  a,b=score(left[c['id']]['answer'],c['expected']),score(right[c['id']]['answer'],c['expected']);rows.append(dict(id=c['id'],expected=c['expected'],left=left[c['id']]['answer'],right=right[c['id']]['answer'],left_f1=round(a['token_f1'],4),right_f1=round(b['token_f1'],4)))
 delta=np.array([r['right_f1']-r['left_f1'] for r in rows]);rng=np.random.default_rng(28);samples=rng.choice(delta,size=(5000,len(delta)),replace=True).mean(axis=1);ci=np.quantile(samples,[.025,.975])
 return rows,dict(left_mean_f1=float(np.mean([x['left_f1'] for x in rows])),right_mean_f1=float(np.mean([x['right_f1'] for x in rows])),paired_delta=float(delta.mean()),bootstrap_95_interval=ci.tolist(),cases=len(rows),seed=28,resamples=5000)
def analyze(p):
 a,b=p.get('left','flan-direct'),p.get('right','flan-context')
 if a not in ['flan-direct','flan-context'] or b not in ['flan-direct','flan-context']:raise ValueError('Unsupported run')
 try:
  cases=json.loads((ROOT/'data/cases.json').read_text());left=json.loads((ROOT/'runs'/f'{a}.json').read_text());right=json.loads((ROOT/'runs'/f'{b}.json').read_text())
 except FileNotFoundError:raise ValueError('No model runs yet. Execute python run_models.py before opening the comparison.')
 rows,m=compare(cases,left['responses'],right['responses'])
 return dict(metrics={'Cases':m['cases'],'Left mean F1':round(m['left_mean_f1'],3),'Right mean F1':round(m['right_mean_f1'],3),'Paired difference':round(m['paired_delta'],3)},rows=rows,bars=[dict(label=a,value=m['left_mean_f1']),dict(label=b,value=m['right_mean_f1'])],notice='Token overlap measures reference agreement, not factuality. Bootstrap intervals assume independent cases; this authored set is too small to establish general superiority.',details={'statistics':m,'left_metadata':left['metadata'],'right_metadata':right['metadata']})
