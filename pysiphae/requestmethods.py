from pysiphae.traversabledict import TraversableDict
from pyramid.renderers import get_renderer
from zope.component import getUtilitiesFor
from pyramid_viewgroup import Provider
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

