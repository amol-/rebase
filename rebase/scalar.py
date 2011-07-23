from base import Entry

class Scalar(Entry):
    __namespace__ = 'scalar'

    def set(self, value):
        self._set(value)

    def get(self):
        return self._get()

    def __eq__(self, other):
        other_value = other
        if isinstance(other_value, Scalar):
            other_value = other._get()
        return self._get() == other_value

class String(Scalar):
    __namespace__ = 'string'

    def __init__(self, field, redis, key=None, value=None):
        super(String, self).__init__(field, redis, key)
        if value:
            self._set(value)

    def _set(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._redis.set(self._key, value)

    def _get(self):
        return self._redis.get(self._key).decode('utf-8')

    def __repr__(self):
        return super(String, self).__repr__() + ' -> ' + repr(self._get())

    def __str__(self):
        return str(self._get())

    def __iter__(self):
        return iter(str(self))

    def __add__(self, op2):
        return str(self) + op2

    def __radd__(self, op1):
        return op1 + str(self)

    def __mul__(self, op):
        return str(self)*op
    __rmul__ = __mul__

    def __mod__(self, param):
        return str(self) % param

    def __iadd__(self, other):
        self._redis.append(self._key, other)
        return self

    def __len__(self):
        return len(str(self))

    def __getitem__(self, pos):
        return str(self)[pos]

    def format(self, params):
        return str(self).format(params)

class Integer(Scalar):
    __namespace__ = 'integer'

    def __init__(self, field, redis, key=None, value=None):
        super(Integer, self).__init__(field, redis, key)
        if value:
            self._set(value)

    def _set(self, value):
        self._redis.set(self._key, value)

    def _get(self):
        return int(self._redis.get(self._key))

    def __int__(self):
        int(self._get())


