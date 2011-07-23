import inspect
from base import Entry, Field
from container import Reference
from scalar import Scalar

class Model(Entry):
    __namespace__ = 'model'

    def __init__(self, field, redis, key=None, **kw):
        super(Model, self).__init__(field, redis, key)

        if not key:
            redis.set(object.__getattribute__(self, '_key'), Model.__namespace__)

        for fieldname, FieldDef in self.__class__.__dict__.iteritems():
            if isinstance(FieldDef, Field):
                prop_key = ':'.join((self._key, fieldname))
                value = FieldDef.new(object.__getattribute__(self, '_redis'), prop_key)
                object.__setattr__(self, fieldname, value)

        for fieldname, fieldvalue in kw.iteritems():
            setattr(self, fieldname, fieldvalue)

    def connect(self, redis):
        self._redis = redis
        for fieldname, obj in self.__dict__.iteritems():
            if isinstance(obj, Entry):
                obj.connect(redis)
        return self

    def __setattr__(self, name, value):
        try:
            obj = object.__getattribute__(self, name)
        except:
            obj = None

        if isinstance(obj, Entry):
            if value is None:
                obj.delete()
            else:
                if isinstance(value, Entry):
                    value = value._get()
                obj._set(value)
        else:
            object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        obj = object.__getattribute__(self, name)
        if isinstance(obj, Scalar) or isinstance(obj, Reference):
            return obj._get()
        else:
            return obj

    def _get(self):
        if self._redis.get(self._key):
            return self
        else:
            return None

    def delete(self):
        super(Model, self).delete()
        for o in self.__dict__.values():
            if isinstance(o, Entry):
                o.delete()

