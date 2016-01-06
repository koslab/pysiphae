from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.types import Integer, Float
from decimal import Decimal
from pysiphae.decorators import storage_factory
from pysiphae.interfaces import ISQLStorage
from zope.interface import implements
from wraptor.decorators import memoize
from datetime import date,datetime

_STORAGES={}

@storage_factory(['mysql','postgresql','hive'])
def sqlalchemy_factory(uri, **options):
    if uri in _STORAGES.keys():
        return _STORAGES[uri]
    storage = SQLAlchemyStorage(uri, **options)
    _STORAGES[uri] = storage
    return storage

def _cast_type(value):
    if isinstance(value, date):
        return value.strftime('%Y-%m-%d')
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%dT%H:%M')
    if isinstance(value, Integer):
        return int(value)
    if isinstance(value, Float):
        return float(value)
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, str):
        return value.decode('utf-8')
    return value

class SQLAlchemyStorage(object):
    implements(ISQLStorage)

    def __init__(self, uri, **options):
        self.engine = create_engine(uri, **options)

    def connect(self, **options):
        self.engine.connect()

    @memoize(instance_method=True)
    def execute(self, query, **options):
        rows = self.engine.execute(text(query), **options)
        keys = rows.keys()
        def clean_prefix(k):
            if '.' in k:
                return '.'.join(k.split('.')[1:])
            return k
        keys = map(clean_prefix, keys)
        result = []
        for r in rows:
            d = {}
            for k,v in zip(keys, r):
                d[k] = _cast_type(v)
            result.append(d)
        return result
   
    def close(self):
        self.engine.dispose() 
