import venusian
from .interfaces import ITemplateVariables

def template_variables(wrapped):
    def callback(scanner, name, obj):
        scanner.config.registry.registerUtility(obj, ITemplateVariables, name)
    venusian.attach(wrapped, callback)
    return wrapped
