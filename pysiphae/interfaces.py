from zope.interface import Interface

class INavigationProvider(Interface):
    pass

class IHomeUrl(Interface):
    pass

class ITemplateVariables(Interface):
    pass

class IStorageFactory(Interface):
    pass

class ISQLStore(Interface):
    def connect(**options): pass
    def execute(query, **options): pass
    def close(): pass

class IObjStore(Interface):
    def connect(**options): pass
    def insert(obj): pass
    def delete(obj): pass
    def update(obj): pass
    def query(**filters): pass
