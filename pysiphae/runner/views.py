from pysiphae.views import Views
from pysiphae.interfaces import IProcessPayload
from pysiphae.interfaces import IProcessManager
from pyramid.view import view_config, forbidden_view_config

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
