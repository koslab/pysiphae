import tornado.ioloop
import tornado.web
from tornado.process import Subprocess
import tornado.websocket
from datetime import datetime
from uuid import uuid4
import json
import tempfile
import os
import base64
import argparse
import copy

_TRACKERS={}
EXECUTORS={}

class ProcessTracker(object):
    
    def __init__(self, processes=None):
        self.processes = processes or {}

    def add(self, key, data):
        d = {'_id': key}
        d.update(data)
        self.processes[key] = d

    def get(self, key):
        return self.processes.get(key, None)

    def delete(self, key):
        if key in self.processes:
            del self.processes[key]

    def all(self):
        return self.processes.values()

def get_process_tracker(group='process.tracker'):
    tracker = _TRACKERS.get(group, None)
    if tracker:
        return tracker

    tracker = ProcessTracker()
    _TRACKERS[group] = tracker
    return tracker

class ProcessSpawner(object):

    def __init__(self, group, registry=None, output_dir=None):
        self.tracker = get_process_tracker(group)
        self.output_dir = tempfile.mkdtemp()
        self.registry = registry or {}

    def spawn(self, command, environ=None, files=None):
        environ=environ or {}
        files = files or []
        _id = uuid4().hex
        process_dir = os.path.join(self.output_dir, _id)
        os.mkdir(process_dir)

        for f in files:
            fpath = os.path.join(process_dir, f['filename'])
            with open(fpath, 'wb') as fd:
                fd.write(base64.b64decode(f['body']))
        outlog = os.path.join(process_dir, 'stdout.log')
        errlog = os.path.join(process_dir, 'stderr.log')

        with open(outlog, 'wb') as out, open(errlog, 'wb') as err:
            if isinstance(command, str):
                command = command.split()
            p = Subprocess(command, env=environ, stdout=out, stderr=err, 
                            cwd=process_dir)

        datum = {
            '_id': _id,
            'pid': p.pid,
            'command': command,
            'stdout': outlog,
            'stderr': errlog,
            'state': 'running',
            'exitcode': None,
            'start': datetime.now().isoformat(),
            'end': None
        }

        def clean(exitcode):
            datum = self.tracker.get(_id)
            datum['state'] = 'stopped'
            datum['exitcode'] = exitcode
            datum['end'] = datetime.now().isoformat()
        p.set_exit_callback(clean)
        self.tracker.add(_id, datum)
        return datum

class ShellExecutor(object):

    def __init__(self, command):
        self.command = command

    def run(self, group, environ, files):
        spawner = ProcessSpawner(group)
        env = copy.deepcopy(os.environ)
        env.update(environ)
        return spawner.spawn(self.command, env, files)

EXECUTORS['shell'] = ShellExecutor

class SpawnHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        executor = data.get('executor', None)
        group = data.get('group', None)
        if not executor or not group:
            raise tornado.web.HTTPError(400)
        options = data.get('options', {})
        environ = data.get('environ', {})
        e = EXECUTORS[executor](**options)
        result = e.run(group, environ, data.get('files', []))
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result, indent=4))

class ProcessList(tornado.web.RequestHandler):
    def get(self):
        result = {}
        for key, tracker in _TRACKERS.items():
            result[key] = tracker.all()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result, indent=4))

    def post(self):
        result = {}
        data = json.loads(self.request.body)
        group = data.get('group')
        tracker = _TRACKERS.get(group, None)
        if tracker:
            result[group] = tracker.all()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result, indent=4))
    

class ProcessDisplay(tornado.web.RequestHandler):
    def get(self, process_id):
        data = None
        for tracker in _TRACKERS.values():
            data = tracker.get(process_id)
            if data: break
        if not data:
            raise tornado.web.HTTPError(404)
        self.set_header("Content-Type", "application/json")
        data['stdout-content'] = open(data['stdout']).read()
        data['stderr-content'] = open(data['stderr']).read()
        self.write(json.dumps(data))

class Tail(tornado.websocket.WebSocketHandler):
    stream = None

    def open(self):
        id_ = self.get_argument('id')
        self.p = Subprocess(['tail','-f', PROCESSES[id_][self.stream]],
                            stdout=Subprocess.STREAM,stderr=Subprocess.STREAM)
        self.p.set_exit_callback(self._close)
        self.p.stdout.read_until('\n', self.write_line)
    
    def _close(self, *args, **kwargs):
        self.close()

    def on_close(self, *args, **kwargs):
        self.p.proc.terminate()
        self.p.proc.wait()

    def write_line(self, data):
        self.write_message(data)
        self.p.stdout.read_until("\n", self.write_line)

class StdoutTail(Tail):
    stream = 'stdout'

class StderrTail(Tail):
    stream = 'stderr'

def make_app():
    return tornado.web.Application([
        (r'/',ProcessList),
        (r"/spawn", SpawnHandler),
        (r'/(\w+)', ProcessDisplay),
        (r'/(\w+)/stdout',StdoutTail),
        (r'/(\w+)/stderr',StderrTail),
    ])

def main():
    parser = argparse.ArgumentParser(
        description='Start Process Manager Daemon')
    parser.add_argument('--port', type=int, help='Port number', default=8888)
    args = parser.parse_args()
    app = make_app()
    port = args.port
    print "Listening on %s" % port
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
