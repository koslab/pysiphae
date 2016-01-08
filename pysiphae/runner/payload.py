from pysiphae.interfaces import IProcessPayload
from zope.interface import implements
import venusian
import asset
import base64
import os
import requests

class Payload(object):
    implements(IProcessPayload)

    def __init__(self, name, executor, files=None, options=None):
        self.name = name
        self.executor = executor
        self.options = options or {}
        self.files = []
        files = files or []
        for f in files:
            fd = asset.load(f)
            fname = os.path.basename(f)
            self.files.append((fname,fd))
        
    def payload(self, request):
        return {
            'files': self.files,
            'json': { 
                'group': self.name,
                'executor': self.executor,
                'options': self.options
            }
        }

    def launch(self, request, url):
        url = url + '/spawn'
        payload = self.payload(request)
        r = requests.post(url, **payload)
        return r.json()

    def processes(self, request, url):
        query = {'group': self.name}
        r = requests.post(url, json=query)
        return r.json().get(self.name, [])


def payload_factory(name, executor='shell', files=None, options=None):
    payload = Payload(name, executor, files, options)
    def callback(scanner, name, obj):
        scanner.config.registry.registerUtility(obj, IProcessPayload, obj.name)
    venusian.attach(payload, callback)
    return payload

echo_payload = payload_factory(
    name='echo',
    executor='shell',
    options={
        'command': ['echo','hello world']   
    })
