import uuid, sys

class NameSpaceException(Exception):
    pass

class MetaEntry(type):
    __namespaces__ = {}
    __classes__ = {}

    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if not classDict.has_key('__namespace__'):
            raise NameSpaceException('%s is missing a namespace' % classname)

        if MetaEntry.__namespaces__.has_key(classDict['__namespace__']):
            raise NameSpaceException('%s namespace is already registered' % classDict['__namespace__'])

        MetaEntry.__namespaces__[classDict['__namespace__']] = cls
        MetaEntry.__classes__[classname] = cls
        return cls

class Entry(object):
    __metaclass__ = MetaEntry
    __namespace__ = 'entry'

    @classmethod
    def new(cls, redis, **params):
        return cls(Field(cls), redis=redis, key=None, **params)

    @classmethod
    def get(cls, redis, key, **params):
        return cls(Field(cls), redis=redis, key=key, **params)

    def __init__(self, field, redis, key=None):
        object.__setattr__(self, '_field', field)
        object.__setattr__(self, '_redis', redis)
        if key:
            object.__setattr__(self, '_key', key)
        else:
            key = '$'.join((self.__class__.__namespace__, str(uuid.uuid1())))
            object.__setattr__(self, '_key', key)

    def connect(self, redis):
        self._redis = redis
        return self
    
    def delete(self):
        self._redis.delete(self._key)

    def __repr__(self):
        return repr(self._key)

    def __nonzero__(self):
        return self._redis.exists(self._key)

class Field(object):
    def __init__(self, FieldType, **kw):
        self.config = kw
        self._FieldType = FieldType

    @property
    def FieldType(self):
        if isinstance(self._FieldType, str):
            self._FieldType = MetaEntry.__classes__[self._FieldType]
        return self._FieldType

    def new(self, redis, key=None):
        return self.FieldType(field=self, redis=redis, key=key, **self.config)