from pyramid.view import view_config, forbidden_view_config
from pyramid.renderers import get_renderer
from pyramid.decorator import reify
from pysiphae.decorators import home_url
from zope.component import getUtilitiesFor
from .interfaces import (INavigationProvider, ITemplateVariables, IHomeUrl)
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (remember, forget,  NO_PERMISSION_REQUIRED)
from repoze.who.api import get_api as get_whoapi
from .security import groupfinder

@home_url
def home_url_from_settings(request, groups):
    settings = request.registry.settings
    s = settings.get('pysiphae.home_urls', '')
    if not s:
        return None
    entries = [i.split('=') for i in s.strip().split('\n')]
    for g, path in entries:
        if g not in groups:
            continue
        return request.resource_url(request.context, path)
    return None

class TraversableDict(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        try:
            result = self.data[key]
        except KeyError:
            raise AttributeError(key)
        if isinstance(result, dict):
            return TraversableDict(result)
        return result

    def __getitem__(self, key):
        return self.data[key]

class Views(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

def main_template(request):
    main_template = get_renderer('templates/main_template.pt').implementation()
    return main_template.macros['master']

def vars(request):
    registry = request.registry
    result = {}
    for name, factory in  registry.getUtilitiesFor(ITemplateVariables):
        result.update(factory(request))
    return TraversableDict(result)

def main_navigation(request):
    links = []
    for name, provider in getUtilitiesFor(INavigationProvider):
        links += provider(request)
    def has_permission(link):
        if link.get('permission', None):
            return request.has_permission(link['permission'])
        return True
    links = filter(has_permission, links)
    links = sorted(links, key=lambda x: x['order'])
    return links


class Pysiphae(Views):

    @view_config(route_name='home', renderer='templates/home.pt')
    def home(self):
        identity = self.request.environ.get('repoze.who.identity', None)
        groups = []
        if identity:
            groups = groupfinder(identity, self.request)
        for name, resolver in self.request.registry.getUtilitiesFor(IHomeUrl):
            url = resolver(self.request, groups)
            if url:
                return HTTPFound(location=url)
        return {}

    @forbidden_view_config(renderer='templates/404.pt')
    def redirect_to_login(self):
        request = self.request
        url = request.url
        login_url = request.resource_url(request.context, 'login')
        identity = request.environ.get('repoze.who.identity', None)
        if not identity:
            return HTTPFound(location='%s?came_from=%s' % (login_url,url))
        return {}
    
    @view_config(route_name='login', renderer='templates/login.pt',
            permission=NO_PERMISSION_REQUIRED)
    def login(self):
        request = self.request
        login_url = request.resource_url(request.context, 'login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/' # never use the login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        who_api = get_whoapi(request.environ)
        if 'form.submitted' in request.params:
            creds = {
                'login':request.params['login'],
                'password': request.params['password']
            }  
            authenticated, headers = who_api.login(creds)
            if authenticated:
                return HTTPFound(location='/', headers=headers)

        message = 'Failed login'

        _, headers = who_api.login({})

        request.response_headerlist = headers
        if 'REMOTE_USER' in request.environ:
            del request.environ['REMOTE_USER']
    
        return dict(
            message = message,
            url = request.application_url + '/login',
            came_from = came_from,
            login = login,
            password = password,
            )
    
    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        who_api = get_whoapi(request.environ)
        headers = who_api.logout()
        url = request.resource_url(request.context)
        return HTTPFound(location=url,headers=headers)
