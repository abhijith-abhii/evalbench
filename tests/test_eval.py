import pytest
from core import score,compare

def test_f1():
 assert score('14 days','14 days')['token_f1']==1
 assert score('14','14 days')['token_f1']==pytest.approx(2/3)
 assert score('','14 days')['token_f1']==0

def test_paired_identity():
 cases=[{'id':'a','expected':'yes'},{'id':'b','expected':'no'}];run={'a':{'answer':'yes'},'b':{'answer':'no'}}
 _,m=compare(cases,run,run);assert m['paired_delta']==0 and m['bootstrap_95_interval']==[0,0]
def test_incomplete_run_rejected():
 with pytest.raises(ValueError):compare([{'id':'a','expected':'x'}],{}, {})
