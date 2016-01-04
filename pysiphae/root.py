from pyramid.security import Allow, Deny, Everyone
import re

class PysiphaeRoot(object):
    __name__ = ''

    def __init__(self, request):
        self.request = request

    @property
    def __acl__(self):
        settings = self.request.registry.settings
        acl = []
        if not ('pysiphae.acl' in settings):
            return [(Allow, Everyone, 'pysiphae.View')]
        for ace in settings['pysiphae.acl'].strip().split('\n'):
            ace = ace.strip()
            if not ace:
                continue
            if ace.startswith('#'):
                continue
            acl.append(ace.split(','))
        return acl

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
        title = settings.get('pysiphae.title','Pysiphae')
        return title

def root_factory(request,*args,**kwargs):
    return PysiphaeRoot(request)
