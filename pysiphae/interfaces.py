from zope.interface import Interface, Attribute

class INavigationProvider(Interface):
    pass

class IHomeUrl(Interface):
    pass

class ITemplateVariables(Interface):
    pass

class IStorageFactory(Interface):
    pass

class IProcessManager(Interface):
    pass

class ISiteRoot(Interface):
    pass

class IProcessPayload(Interface):
    name = Attribute('Name')
    type = Attribute('Type of payload (eg: pyspark, hive)')
    files = Attribute('List of path of files to submit')
    options = Attribute('Mapping of additional options to pass to executor')

class ISQLStorage(Interface):
    def connect(**options): pass
    def execute(query, **options): pass
    def close(): pass

class IObjStorage(Interface):
    def connect(**options): pass
    def insert(obj): pass
    def delete(obj): pass
    def update(obj): pass
    def query(**filters): pass


class IViewletManager(Interface):
    pass
