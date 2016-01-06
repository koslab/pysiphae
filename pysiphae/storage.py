from urlparse import urlparse, parse_qs
from .interfaces import IStorageFactory

def connect(registry, uri, **options):
    """
    parse connection uri and return a Storage object
    """

    parsed = urlparse(uri)
    factory = registry.getUtility(IStorageFactory, name=parsed.scheme)
    return factory(uri, **options)
