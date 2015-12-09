from pyramid.config import Configurator
from ConfigParser import ConfigParser

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    for route in _get_routes(global_config['__file__']):
        config.add_route(route['name'], route['pattern'])
    config.scan()
    for plugin in _get_plugins(global_config['__file__']):
        config.scan(plugin)

    return config.make_wsgi_app()

def _get_plugins(configfile):
    cp = ConfigParser()
    cp.readfp(open(configfile))
    if not cp.has_section('pysiphae'):
        return []
    if not cp.has_option('pysiphae','plugins'):
        return []
    return cp.get('pysiphae','plugins').strip().split()

def _get_routes(configfile):
    cp = ConfigParser()
    cp.readfp(open(configfile))
    if not cp.has_section('pysiphae'):
        return []
    if not cp.has_option('pysiphae','routes'):
        return []
    v = cp.get('pysiphae','routes')
    vv = [x.split() for x in v.strip().split('\n')]
    return [{'name': x[0], 'pattern': x[1]} for x in vv]
