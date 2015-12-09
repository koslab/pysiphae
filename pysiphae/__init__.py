from pyramid.config import Configurator
from ConfigParser import ConfigParser
from zope.component import getSiteManager

def import_class(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
#    config.hook_zca()
#    config.include('pyramid_zcml')
    config.include('pyramid_chameleon')
    config.add_static_view('++static++', 'static', cache_max_age=3600)

    cp = ConfigParser()
    cp.readfp(open(global_config['__file__']))

    for route in _get_routes(cp):
        config.add_route(route['name'], route['pattern'])
    config.scan()

    plugins = _get_plugins(cp)
    for plugin in plugins:
        config.scan(plugin)
#        config.load_zcml(plugin + ':configure.zcml')

    return config.make_wsgi_app()

def _get_plugins(cp):
    if not cp.has_section('pysiphae'):
        return []
    if not cp.has_option('pysiphae','plugins'):
        return []
    return cp.get('pysiphae','plugins').strip().split()

def _get_routes(cp):
    if not cp.has_section('pysiphae'):
        return []
    if not cp.has_option('pysiphae','routes'):
        return []
    v = cp.get('pysiphae','routes')
    vv = [x.split() for x in v.strip().split('\n')]
    return [{'name': x[0], 'pattern': x[1]} for x in vv]

def _get_adapters(cp):
    if not cp.has_section('pysiphae'):
        return []
    if not cp.has_option('pysiphae','routes'):
        return []
    v = cp.get('pysiphae','routes')
    vv = [x.split() for x in v.strip().split('\n')]
    return [{'name': x[0], 'pattern': x[1]} for x in vv]
