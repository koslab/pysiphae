from templer.core import BasicNamespace
import copy

class Project(BasicNamespace):
    _template_dir = 'templates/project'
    summary = 'Skeleton for Pysiphae Project'
    help = """This creates a python project with Pysiphae"""
    category = 'Pysiphae'
    default_required_structures = []
    vars = copy.deepcopy(BasicNamespace.vars)
    for v in vars:
        if v.name=='license_name':
            v.default='MIT'
        if v.name=='url':
            v.default='http://github.com/'
