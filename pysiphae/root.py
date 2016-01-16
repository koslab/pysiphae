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

    def isAnonymous(self):
        identity = self.request.environ.get('repoze.who.identity', None)
        return False if identity else True

    def getAuthenticatedUser(self):
        identity = self.request.environ.get('repoze.who.identity', None)
        if not identity:
            return {}
        identity = dict(identity)
        userid = identity.get('repoze.who.userid', '')
        if not userid:
            return {}
        if re.match(r'(\w+=.+,?)+', userid):
            userid = userid.split(',')[0].split('=')[1]
        return {
            'userid': userid,
            'identity': identity
        }

    @property
    def title(self):
        settings = self.request.registry.settings
        title = settings['pysiphae'].get('title','Pysiphae')
        return title

def root_factory(request,*args,**kwargs):
    return PysiphaeRoot(request)
