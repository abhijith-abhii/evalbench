from pathlib import Path
import os
os.environ.setdefault('HF_HOME', str(Path(__file__).resolve().parent/'var/hf-cache'))
import os,json,time
from pathlib import Path
import torch
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
ROOT=Path(__file__).parent;torch.set_num_threads(4);torch.manual_seed(28)
name='google/flan-t5-small';rev='0fc9ddf78a1e988dac52e2dac162b0ede4fd74ab';source=os.environ.get('EVAL_MODEL',name);kwargs={} if Path(source).exists() else {'revision':rev}
tok=AutoTokenizer.from_pretrained(source,**kwargs);model=AutoModelForSeq2SeqLM.from_pretrained(source,**kwargs).eval();cases=json.loads((ROOT/'data/cases.json').read_text());(ROOT/'runs').mkdir(exist_ok=True)
for run in ['flan-direct','flan-context']:
 responses={}
 for case in cases:
  prompt=('Use this context to answer. If the answer is not stated, say unknown. Context: '+case['context']+'\n' if run=='flan-context' else '')+'Question: '+case['question']+'\nShort answer:'
  encoded=tok(prompt,return_tensors='pt');start=time.perf_counter()
  with torch.no_grad():out=model.generate(**encoded,max_new_tokens=35,do_sample=False)
  responses[case['id']]={'answer':tok.decode(out[0],skip_special_tokens=True),'seconds':round(time.perf_counter()-start,4),'input_tokens':int(encoded.input_ids.numel()),'output_tokens':int(out.numel()),'api_cost_usd':0}
 result={'metadata':{'model':name,'revision':rev,'run':run,'actual_inference':True,'device':'CPU','seed':28,'max_new_tokens':35,'cost_note':'No paid API; local electricity/hardware cost not measured'},'responses':responses}
 (ROOT/'runs'/f'{run}.json').write_text(json.dumps(result,indent=2));print(run,flush=True)
