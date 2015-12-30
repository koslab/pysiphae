from pyramid.security import Allow, Deny, Everyone

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

def root_factory(request,*args,**kwargs):
    return PysiphaeRoot(request)
