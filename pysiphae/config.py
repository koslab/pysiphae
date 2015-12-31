from .decorators import template_variables
from zope.component.hooks import getSite

def get_portal(context):
    if getattr(context, '__parent__', None):
        return get_portal(context.__parent__)
    return context

@template_variables
def get_template_variables(request):
    identity = request.environ.get('repoze.who.identity', None)
    portal = get_portal(request.context)
    return {
        'isAnonymous' : False if identity else True,
        'portal': portal
    }
