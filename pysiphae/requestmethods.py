from pysiphae.traversabledict import TraversableDict
from pyramid.renderers import get_renderer
from zope.component import getUtilitiesFor
from pyramid_viewgroup import Provider
from pysiphae.decorators import request_method
import re, json
from .interfaces import (INavigationProvider, ITemplateVariables, IHomeUrl)

def main_template(request):
    main_template = get_renderer('templates/main_template.pt').implementation()
    return main_template.macros['master']

def pconfig(request):
    pconfig = request.registry.settings.get('pysiphae', {})
    return pconfig

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

def viewgroup_provider(request):
    return Provider(request.context, request)

@request_method('getAuthenticatedUser')
def getAuthenticatedUser(request):
    identity = request.environ.get('repoze.who.identity', None)
    if not identity:
        return {}
    identity = dict(identity)
    user = identity.get('repoze.who.userid', '')
    if not user:
        return {}

    userid = user
    if re.match(r'(\w+=.+,?)+', userid):
        userid = userid.split(',')[0].split('=')[1]
    return {
        'userid': userid,
        'identity': identity,
    }

@request_method('isAnonymous')
def isAnonymous(request):
    identity = request.environ.get('repoze.who.identity', None)
    return False if identity else True

@request_method('flash_message')
def flash_message(request, type, message):
    request.session.flash(json.dumps({'type': type, 'message': message}))

@request_method('pop_messages')
def pop_messages(request):
    flashes = request.session.pop_flash()
    result = [json.loads(flash) for flash in flashes]
    for i in result:
        i['class'] = i['type']
        if i['type'] == 'error':
            i['class'] = 'danger'
    return result
