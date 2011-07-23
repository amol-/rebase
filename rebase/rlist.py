from base import Entry
from container import Container

class List(Container):
    __namespace__ = 'list'

    def __init__(self, field, redis, contains, key=None):
        super(List, self).__init__(field, redis, contains, key)

    def _set(self, value):
        self._redis.delete(self._key)
        for k in value:
            self.append(v)

    def _get(self):
        entries = self._redis.lrange(self._key, 0, -1)
        return [self._castback(entry) for entry in entries]

    def append(self, obj):
        self._redis.rpush(self._key, self._cast(obj))

    def deleteall(self):
        for e in self:
            if isinstance(e, Entry):
                try:
                    e.deleteall()
                except:
                    e.delete()
        self.delete()

    def __setitem__(self, k, v):
        self._redis.lset(self._key, k, self._cast(v))

    def __getitem__(self, k):
        entry = self._redis.lrange(self._key, k, k)
        if not entry:
            return None
        else:
            return self._castback(entry[0])

    def __len__(self):
        return self._redis.llen(self._key)

    def __repr__(self):
        return repr(self._get())

    def __iter__(self):
        class ListIterator(object):
            def __init__(self, list):
                self.index = 0
                self.list = list

            def next(self):
                if self.index >= len(self.list):
                    raise StopIteration
                else:
                    i = self.list[self.index]
                    self.index += 1
                    return i

        return ListIterator(self)

