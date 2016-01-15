from pyramid.security import NO_PERMISSION_REQUIRED
from pysiphae.interfaces import IProcessPayload
from pysiphae.interfaces import IProcessManager
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import json

class RunnerViews(object):
    
    @view_config(route_name='pysiphae.processmgr', 
            renderer='templates/runner.pt',
            permission='pysiphae.processmgr.View')
    def runner_view(self):
        registry = self.request.registry
        payload_name = self.request.params.get('payload', None)
        if payload_name:
            payload = registry.getAdapter(self.request, IProcessPayload, name=payload_name)
            api = self.request.registry.getUtility(IProcessManager,
                    name=payload.server)
            res = payload.launch(self.request, api)
            return HTTPFound(location=self.request.path)
        payloads = self.request.registry.getAdapters((self.request,), IProcessPayload)
        # only allow authorized payloads
        payloads = [p for p in payloads if (
            p[1].permission == NO_PERMISSION_REQUIRED or
            self.request.has_permission(p[1].permission, self.context))]
        result = []
        for name, payload in payloads:
            api = self.request.registry.getUtility(IProcessManager,
                    name=payload.server)
            procs = payload.processes(self.request, api)
            running = len([i for i in procs if i['state'] == 'running'])
            stopped = len([i for i in procs if i['state'] == 'stopped'])
            result.append({
                'name': name,
                'description': payload.description,
                'type': payload.executor,
                'running': running,
                'stopped': stopped
            })
        return {
            'payloads': result
        }

    @view_config(route_name='pysiphae.processmgr.group', 
            renderer='templates/group.pt',
            permission='pysiphae.processmgr.View')
    def group_view(self):
        name = self.request.matchdict['name']
        payload = self.request.registry.getAdapter(self.request, IProcessPayload, name=name)
        api = self.request.registry.getUtility(IProcessManager,
                name=payload.server)
        procs = api.processes(name).get(name, [])
        procs = sorted(procs, key=lambda x: x['start'], reverse=True)
        return {
            'name': name,
            'processes': procs
        }

    @view_config(route_name='pysiphae.processmgr.process', 
            renderer='templates/process.pt',
            permission='pysiphae.processmgr.View')
    def process_view(self):
        name = self.request.matchdict['name']
        process_id = self.request.matchdict['process_id']
        payload = self.request.registry.getAdapter(self.request, IProcessPayload, name=name)
        api = self.request.registry.getUtility(IProcessManager,
                name=payload.server)
        process_data = api.process(process_id)
        return {
            'name': name,
            'id': process_id,
            'start': process_data['start'],
            'end': process_data['end'],
            'stdout': process_data['stdout-content'],
            'stderr': process_data['stderr-content']
        }

