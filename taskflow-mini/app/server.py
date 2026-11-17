from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

ROOT = Path(__file__).parent

def add_task(tasks, title):
    title = title.strip()
    if not title:
        raise ValueError('Task cannot be empty')
    return tasks + [{'id': len(tasks) + 1, 'title': title}]

class Handler(BaseHTTPRequestHandler):
    tasks = []
    def do_GET(self):
        if self.path == '/health':
            self.respond(200, {'status': 'ok'})
        elif self.path == '/api/tasks':
            self.respond(200, self.tasks)
        elif self.path == '/':
            data = (ROOT / 'index.html').read_bytes()
            self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
        else: self.respond(404, {'error':'not found'})
    def do_POST(self):
        if self.path != '/api/tasks': return self.respond(404, {'error':'not found'})
        try:
            size = int(self.headers.get('Content-Length','0'))
            payload = json.loads(self.rfile.read(size))
            self.__class__.tasks = add_task(self.tasks, payload.get('title',''))
            self.respond(201, self.tasks[-1])
        except (ValueError, json.JSONDecodeError, AttributeError) as exc:
            self.respond(400, {'error':str(exc)})
    def respond(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)

if __name__ == '__main__':
    print('Open http://localhost:8000', flush=True)
    HTTPServer(('127.0.0.1',8000), Handler).serve_forever()
