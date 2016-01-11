from pysiphae.views import Views
from pysiphae.interfaces import IProcessPayload
from pysiphae.interfaces import IProcessManager
from pyramid.view import view_config, forbidden_view_config
import json

class RunnerViews(Views):
    
    @view_config(route_name='pysiphae.runner', 
            renderer='templates/runner.pt',
            permission='pysiphae.ViewRunner')
    def runner_view(self):
        registry = self.request.registry
        payload_name = self.request.params.get('payload', None)
        api = self.request.registry.getUtility(IProcessManager)
        if payload_name:
            payload = registry.getUtility(IProcessPayload, name=payload_name)
            res = payload.launch(self.request, api)
        payloads = self.request.registry.getUtilitiesFor(IProcessPayload)
        result = []
        for name, payload in payloads:
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

    @view_config(route_name='pysiphae.runner.group', 
            renderer='templates/group.pt',
            permission='pysiphae.ViewRunner')
    def group_view(self):
        name = self.request.matchdict['name']
        api = self.request.registry.getUtility(IProcessManager)
        procs = api.processes(name).get(name, [])
        procs = sorted(procs, key=lambda x: x['start'], reverse=True)
        return {
            'name': name,
            'processes': procs
        }

    @view_config(route_name='pysiphae.runner.process', 
            renderer='templates/process.pt',
            permission='pysiphae.ViewRunner')
    def process_view(self):
        name = self.request.matchdict['name']
        process_id = self.request.matchdict['process_id']
        api = self.request.registry.getUtility(IProcessManager)
        process_data = api.process(process_id)
        return {
            'name': name,
            'id': process_id,
            'start': process_data['start'],
            'end': process_data['end'],
            'stdout': process_data['stdout-content'],
            'stderr': process_data['stderr-content']
        }

