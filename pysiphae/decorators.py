import venusian
from .interfaces import (
        ITemplateVariables, 
        IHomeUrl, 
        IStorageFactory,
        INavigationProvider)

def template_variables(wrapped):
    def callback(scanner, name, obj):
        nm = '%s.%s' % (obj.__module__, name)
        scanner.config.registry.registerUtility(obj, ITemplateVariables, nm)
    venusian.attach(wrapped, callback)
    return wrapped

def home_url(wrapped):
    def callback(scanner, name, obj):
        nm = '%s.%s' % (obj.__module__, name)
        scanner.config.registry.registerUtility(obj, IHomeUrl, nm)
    venusian.attach(wrapped, callback)
    return wrapped

def navigation(wrapped):
    def callback(scanner, name, obj):
        nm = '%s.%s' % (obj.__module__, name)
        scanner.config.registry.registerUtility(obj, INavigationProvider, nm)
    venusian.attach(wrapped, callback)
    return wrapped

def storage_factory(schemes):
    if not hasattr(schemes, '__iter__'):
        schemes = [schemes]
    def decorator(wrapped):
        def callback(scanner, name, obj):
            for scheme in schemes:
                scanner.config.registry.registerUtility(
                        obj, IStorageFactory, scheme)
        venusian.attach(wrapped, callback)
        return wrapped
    return decorator
