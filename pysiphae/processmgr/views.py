from pyramid.security import NO_PERMISSION_REQUIRED
from pysiphae.interfaces import IProcessPayload
from pysiphae.interfaces import IProcessManager
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import json

@view_config(route_name='pysiphae.processmgr', 
        renderer='templates/runner.pt',
        permission='pysiphae.processmgr.View')
def runner_view(context, request):
    registry = request.registry
    payload_name = request.params.get('payload', None)
    if payload_name:
        payload = registry.getAdapter(request, IProcessPayload, name=payload_name)
        api = request.registry.getUtility(IProcessManager,
                name=payload.server)
        res = payload.launch(request, api)
        return HTTPFound(location=request.path)
    payloads = request.registry.getAdapters((request,), IProcessPayload)
    # only allow authorized payloads
    payloads = [p for p in payloads if (
        p[1].permission == NO_PERMISSION_REQUIRED or
        request.has_permission(p[1].permission, context))]
    result = []
    for name, payload in payloads:
        api = request.registry.getUtility(IProcessManager,
                name=payload.server)
        procs = payload.processes(request, api)
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
def group_view(context, request):
    name = request.matchdict['name']
    payload = request.registry.getAdapter(request, IProcessPayload, name=name)
    api = request.registry.getUtility(IProcessManager,
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
def process_view(context, request):
    name = request.matchdict['name']
    process_id = request.matchdict['process_id']
    payload = request.registry.getAdapter(request, IProcessPayload, name=name)
    api = request.registry.getUtility(IProcessManager,
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

