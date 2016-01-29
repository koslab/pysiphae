from pyramid.security import Allow, Deny, Everyone
from pysiphae.interfaces import ISiteRoot
from zope.interface import implements
import re

class PysiphaeRoot(object):
    implements(ISiteRoot)

    __name__ = ''

    def __init__(self, request):
        self.request = request

    @property
    def __acl__(self):
        settings = self.request.registry.settings
        if not ('acl' in settings['pysiphae']):
            return [(Allow, Everyone, settings['pysiphae']['default_permission'])]
        return settings['pysiphae']['acl']

    @property
    def title(self):
        settings = self.request.registry.settings
        title = settings['pysiphae'].get('title','Pysiphae')
        return title

def root_factory(request,*args,**kwargs):
    return PysiphaeRoot(request)
