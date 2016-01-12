from pysiphae.interfaces import IProcessPayload, IProcessManager
from zope.interface import implements
import venusian
import asset
import base64
import os
import requests
from urlparse import urlparse, ParseResult
from pyramid.security import NO_PERMISSION_REQUIRED

class ProcessManager(object):
    implements(IProcessManager)

    def __init__(self, url):
        self._url = url

    def url(self, path=''):
        parsed = urlparse(self._url)
        p = parsed.path.split('/')
        p += path.replace('/',' ').strip().split()
        d = parsed._asdict()
        d['path'] = '/'.join(p)
        return ParseResult(**d).geturl()

    def processes(self, group=None):
        params = {}
        if group:
            params['group'] = group
        r = requests.get(self.url(), json=params)
        return r.json()

    def process(self, identifier):
        url = self.url(identifier)
        r = requests.get(url)
        return r.json()

    def spawn(self, payload):
        url = self.url('spawn')
        r = requests.post(url, json=payload)
        return r.json()


class Payload(object):
    implements(IProcessPayload)

    def __init__(self, name, description, 
                       executor, files=None, options=None, permission=None):
        self.name = name
        self.description = description
        self.executor = executor
        self.options = options or {}
        self.files = files or []
        self.permission = permission or NO_PERMISSION_REQUIRED
        
    def payload(self, request):
        files = []
        for f in self.files:
            a = asset.load(f)
            fd = open(a.filename, 'rb')
            fname = os.path.basename(a.filename)
            files.append({
                'filename': fname,
                'body': base64.b64encode(fd.read())
            })
        return {
            'group': self.name,
            'executor': self.executor,
            'options': self.options,
            'files': files
        }

    def launch(self, request, api):
        return api.spawn(self.payload(request))

    def processes(self, request, api):
        return api.processes(group=self.name).get(self.name, [])

def factory(name, description, executor='shell', files=None, options=None,
        permission=None):
    payload = Payload(name, description, executor, files, options, permission)
    def callback(scanner, name, obj):
        scanner.config.registry.registerUtility(obj, IProcessPayload, obj.name)
    venusian.attach(payload, callback)
    return payload
