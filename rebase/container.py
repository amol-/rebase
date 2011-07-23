import inspect
from base import Entry

class Container(Entry):
    __namespace__ = 'container'

    def __init__(self, field, redis, contains, key=None):
        super(Container, self).__init__(field, redis, key)
        self.contains = contains

    def _cast(self, value):
        if inspect.isclass(self.contains.FieldType) and issubclass(self.contains.FieldType, Entry):
            value = value._key
        return value

    def _castback(self, value):
        if inspect.isclass(self.contains.FieldType):
            if issubclass(self.contains.FieldType, Entry):
                value = self.contains.new(self._redis, value)
                if not value:
                    return None
            else:
                value = self.contains.FieldType(value)
        return value

class Reference(Container):
    __namespace__ = 'reference'

    def __init__(self, field, redis, contains, key=None, entry=None):
        super(Reference, self).__init__(field, redis, contains, key)
        if entry:
            self._set(entry)

    def _set(self, entry):
        if entry is not None:
            self._redis.set(self._key, entry._key)
        else:
            self._redis.delete(self._key)

    def _get(self):
        data = self._redis.get(self._key)
        if data is None:
            return None

        return self.contains.new(self._redis, key=data)._get()

def ref(entry):
    return Reference(None, entry._redis, entry._field, entry=entry)

