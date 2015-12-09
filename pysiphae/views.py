from pyramid.view import view_config
from pyramid.renderers import get_renderer

class Views(object):

    project_title = 'Pysiphae'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def main_template(self):
        main_template = get_renderer('templates/main_template.pt').implementation()
        return main_template.macros['master']


class Home(Views):

    @view_config(route_name='home', renderer='templates/home.pt')
    def my_view(self):
        return {'view': self}
    
