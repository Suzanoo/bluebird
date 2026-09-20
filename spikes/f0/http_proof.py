"""Local synchronous transport proof only; not a deployed/production server."""
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,parse_qs
from run import convert
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=4_000_000:raise ValueError('Expected XML up to 4 MB')
            method=parse_qs(urlparse(self.path).query).get('method',[''])[0]
            field=parse_qs(urlparse(self.path).query).get('msp_activity_id_field',[None])[0]
            data,_=convert(self.rfile.read(n),method,field)
        except Exception:
            self.send_error(422,'Invalid or unsupported F0 request');return
        self.send_response(200);self.send_header('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');self.send_header('Content-Disposition','attachment; filename="progress-f0.xlsx"');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
# Documented file-based Python runtime handler name; deployment remains untested.
handler = Handler
if __name__=='__main__':HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
