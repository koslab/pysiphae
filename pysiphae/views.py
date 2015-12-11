from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.decorator import reify
from zope.component import getUtilitiesFor
from .interfaces import INavigationProvider

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
