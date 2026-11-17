from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

ROOT = Path(__file__).parent

def add_task(tasks, title):
    title = title.strip()
    if not title:
        raise ValueError('Task cannot be empty')
    return tasks + [{'id': len(tasks) + 1, 'title': title, 'completed': False}]

def completed_task_count(tasks):
    return sum(task.get('completed', False) for task in tasks)

def set_task_completed(tasks, task_id, completed):
    for task in tasks:
        if task['id'] == task_id:
            return [
                {**item, 'completed': completed} if item['id'] == task_id else item
                for item in tasks
            ]
    raise ValueError('Task not found')

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
    def do_PATCH(self):
        if not self.path.startswith('/api/tasks/'): return self.respond(404, {'error':'not found'})
        try:
            task_id = int(self.path.rsplit('/', 1)[-1])
            size = int(self.headers.get('Content-Length','0'))
            payload = json.loads(self.rfile.read(size))
            completed = payload['completed']
            if not isinstance(completed, bool):
                raise ValueError('Completed must be a boolean')
            self.__class__.tasks = set_task_completed(self.tasks, task_id, completed)
            task = next(item for item in self.tasks if item['id'] == task_id)
            self.respond(200, task)
        except (ValueError, KeyError, json.JSONDecodeError, AttributeError) as exc:
            self.respond(400, {'error':str(exc)})
    def respond(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)

if __name__ == '__main__':
    print('Open http://localhost:8000', flush=True)
    HTTPServer(('127.0.0.1',8000), Handler).serve_forever()
