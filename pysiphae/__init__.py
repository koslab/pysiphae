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
    config.hook_zca()
    config.include('pyramid_zcml')
    config.load_zcml('pysiphae:configure.zcml')
    config.include('pyramid_chameleon')
    config.add_static_view('++static++', 'static', cache_max_age=3600)
    config.add_route('home','/')
    config.scan()

    plugins = settings.get('pysiphae.plugins', '').strip().split()
    for plugin in plugins:
        config.scan(plugin)
        config.load_zcml(plugin + ':configure.zcml')

    return config.make_wsgi_app()
