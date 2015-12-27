from zope.interface import Interface

class INavigationProvider(Interface):

    def get_links(self):
        """
        returns a list of links in the following format
        
        [{'label': 'hello world', 'href': '/path/to/somewhere' , 'order': 1}, 
           ... ]
        """
        pass

class IHomeViewResolver(Interface):

    def resolve(request, groups):
        pass
