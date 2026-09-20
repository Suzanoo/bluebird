"""Synthetic capacity samples, each measured in a fresh process."""
import subprocess,sys,json
from pathlib import Path
from datetime import date,timedelta
ROOT=Path(__file__).parent
out=ROOT/'evidence';out.mkdir(exist_ok=True)
results=[]
for label,n,periods in [('small',2,8),('typical',200,104),('large',1000,156)]:
    finish=date(2026,1,5)+timedelta(days=7*periods-1)
    tasks=''.join(f'<Task><UID>{i+2}</UID><ID>{i+1}</ID><Name>Activity {i+1}</Name><OutlineLevel>2</OutlineLevel><Summary>0</Summary><Start>2026-01-05T08:00:00</Start><Finish>{finish}T17:00:00</Finish><Duration>PT{8*(i%20+1)}H0M0S</Duration><DurationFormat>7</DurationFormat></Task>' for i in range(n))
    raw=('<Project><Name>Synthetic capacity only</Name><Tasks><Task><UID>1</UID><Summary>1</Summary><OutlineLevel>1</OutlineLevel><WBS>1</WBS><Name>All work</Name></Task>'+tasks+'</Tasks></Project>').encode()
    xml=out/(label+'.xml');xml.write_bytes(raw)
    r=subprocess.run([sys.executable,str(ROOT/'run.py'),str(xml),str(out/(label+'.xlsx')),'--method','Duration'],capture_output=True,text=True,check=True)
    result=json.loads(r.stdout);result.update(profile=label,periods=periods);results.append(result);print(json.dumps(result),flush=True)
(out/'benchmark.json').write_text(json.dumps(results,indent=2)+'\n')
