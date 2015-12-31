import venusian
from .interfaces import ITemplateVariables, IHomeUrl

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
