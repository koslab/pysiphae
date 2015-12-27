from pyramid.config import Configurator
from ConfigParser import ConfigParser
from zope.component import getSiteManager
from pysiphae.root import root_factory
from .interfaces import IConfigurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.hook_zca()
    config.include('pyramid_zcml')
    config.load_zcml('pysiphae:configure.zcml')
    config.include('pyramid_chameleon')
    config.set_default_permission('pysiphae.view')
    config.set_root_factory(root_factory)
    config.add_static_view('++static++', 'static', cache_max_age=3600)
    config.add_route('home','/')
    config.add_route('login','/login')
    config.add_route('logout','/logout')
    config.scan()

    plugins = settings.get('pysiphae.plugins', '').strip().split()
    for plugin in plugins:
        config.scan(plugin)
        config.load_zcml(plugin + ':configure.zcml')
        package = config.maybe_dotted(plugin)
        if getattr(package, 'configure'):
            package.configure(config, settings)

    return config.make_wsgi_app()

