from urlparse import urlparse, parse_qs
from .interfaces import IStorageFactory

def connect(uri, registry, **options):
    """
    parse connection uri and return a Storage object
    """

    parsed = urlparse(uri)
    factory = registry.getUtility(IStorageFactory, name=parsed.scheme)
    return factory(uri, registry, **options)
