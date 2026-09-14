import argparse,json,time,platform
try:
    import resource
except ImportError:
    resource = None
from pathlib import Path
from model import parse_xml,normalize
from workbook import render

def convert(raw,method,msp_activity_id_field=None):
    t=time.perf_counter();root=parse_xml(raw);p=time.perf_counter()
    schedule=normalize(root,raw,msp_activity_id_field=msp_activity_id_field);n=time.perf_counter();data=render(schedule,method);e=time.perf_counter()
    return data,dict(activities=len(schedule.activities),parse_s=p-t,normalize_s=n-p,workbook_s=e-n,total_s=e-t,peak_rss_mib=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024 if platform.system()=='Darwin' else 1024) if resource else None),xml_bytes=len(raw),xlsx_bytes=len(data),python=platform.python_version(),method=method)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('xml');p.add_argument('output');p.add_argument('--method',choices=['Equal','Duration'],required=True);p.add_argument('--msp-activity-id-field');a=p.parse_args()
    data,metrics=convert(Path(a.xml).read_bytes(),a.method,a.msp_activity_id_field);Path(a.output).write_bytes(data);print(json.dumps(metrics,sort_keys=True))
