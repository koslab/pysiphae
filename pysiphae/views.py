from pyramid.view import view_config, forbidden_view_config
from pyramid.renderers import get_renderer
from pyramid.decorator import reify
from zope.component import getUtilitiesFor
from .interfaces import INavigationProvider
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (remember, forget)
from repoze.who.api import get_api as get_whoapi

class Views(object):

    project_title = 'Pysiphae'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def main_template(self):
        main_template = get_renderer('templates/main_template.pt').implementation()
        return main_template.macros['master']

    @property
    def main_navigation(self):
        links = []
        for name,util in getUtilitiesFor(INavigationProvider):
            links += util.get_links()
        links = sorted(links, key=lambda x: x['order'])
        return links


class Pysiphae(Views):

    @view_config(route_name='home', renderer='templates/home.pt')
    def home(self):
        return {'view': self}

    
    @view_config(route_name='login', renderer='templates/login.pt')
    @forbidden_view_config(renderer='templates/login.pt')
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
