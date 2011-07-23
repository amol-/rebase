from base import Entry
from container import Container

class Dictionary(Container):
    __namespace__ = 'dictionary'

    def __init__(self, field, redis, contains, key=None):
        super(Dictionary, self).__init__(field, redis, contains, key)

    def _set(self, value):
        self._redis.delete(self._key)
        for k in value:
            self[k] = v

    def _get(self):
        return dict((key, self._castback(value)) for key, value in self._redis.hgetall(self._key))

    def deleteall(self):
        print 'Deleting Dict', self._key, len(self)
        for k, v in self.iteritems():
            print 'Deleting', k, v
            if isinstance(v, Entry):
                try:
                    v.deleteall()
                except:
                    v.delete()
        self.delete()

    def __setitem__(self, k, v):
        self._redis.hset(self._key, k, self._cast(v))

    def __getitem__(self, k):
        if not self._redis.hexists(self._key, k):
            raise KeyError(k)
        return self._castback(self._redis.hget(self._key, k))

    def __delitem__(self, k):
        self._redis.hdel(self._key, k)

    def __len__(self):
        return self._redis.hlen(self._key)

    def has_key(self, k):
        return self._redis.hexists(self._key, k)

    def keys(self):
        return self._redis.hkeys(self._key)

    def items(self):
        return self._get().items()

    def iteritems(self):
        return ((k, self[k]) for k in self.keys())

    def values(self):
        return [self._castback(v) for v in self._redis.hvals(self._key)]

