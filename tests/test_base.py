# -*- coding: utf-8 -*-

import redis
from nose.tools import raises

from rebase import Entry, String, Field, Reference, ref
from rebase.base import MetaEntry


class TestEntry(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', port=6379)

    def teardown(self):
        assert not self.redis.keys()

    def test_key(self):
        o = Entry(None, self.redis, 'key')
        assert o._key == 'key'

    def test_keygen(self):
        o = Entry(None, self.redis)
        assert isinstance(o._key, str)

    def test_delete(self):
        o = Entry(None, self.redis)
        self.redis.set(o._key, 'value')
        o.delete()
        assert not self.redis.exists(o._key)

    def test_namespaces(self):
        for ns in ['string', 'reference', 'list', 'dictionary', 'scalar', 'integer', 'entry', 'model']:
            assert ns in MetaEntry.__namespaces__


class TestReference(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', port=6379)

    def teardown(self):
        assert not self.redis.keys()

    def test_reference(self):
        s = String.new(self.redis, value='Hello World')
        r = ref(s)
        assert r._get() == s._get()
        s.delete()
        r.delete()

    def test_reference_as_class(self):
        s = String.new(self.redis, value='Hello World')
        r = Reference.new(self.redis, contains=Field(String), entry=s)
        assert r._get() == s._get()
        s.delete()
        r.delete()

    def test_reference_with_string(self):
        s = String.new(self.redis, value='Hello World')
        r = Reference.new(self.redis, contains=Field('String'), entry=s)
        assert r._get() == s._get()
        s.delete()
        r.delete()

class TestStringEntity(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', port=6379)

    def teardown(self):
        assert not self.redis.keys()

    def test_set_and_delete(self):
        s = String.new(self.redis)
        s.set('hello world')
        assert self.redis.get(s._key) == 'hello world'
        s.delete()
        assert not self.redis.exists(s._key)

    def test_set_and_get(self):
        s = String.new(self.redis)
        s._set('Hello World')
        assert s == 'Hello World', s._get()
        s.delete()

    def test_constructor(self):
        s = String.new(self.redis, value='Hello World')
        assert s == 'Hello World', s._get()
        s.delete()

    def test_unicode(self):
        s = String.new(self.redis, value=u'àèìòù')
        assert s == u'àèìòù', s._get()
        s.delete()
    
    def test_concat(self):
        s = String.new(self.redis, value='Hello World')
        assert ('hi, ' + s) == 'hi, Hello World'
        assert (s + ' dude') == 'Hello World dude'
        s.delete()

    def test_operators(self):
        s = String.new(self.redis, value='Hello World')

        assert s*3 == 'Hello World'*3       
        s+=' dude'
        assert s == 'Hello World dude'

        s.delete()  
    
    def test_slicing(self):
        s = String.new(self.redis, value='Hello World')
        assert s[1:3] == 'el', s[1:3]
        s.delete()

    def test_format(self):
        s = String.new(self.redis, value='Hello {0} %s')
        assert s % 'World' == 'Hello {0} World'
        assert s.format('World') == 'Hello World %s'
        s.delete()

    def test_iter(self):
        s = String.new(self.redis, value='Hello')
        assert len(list(iter(s))) == 5
        for i, c in enumerate(s):
            assert c == 'Hello'[i]
        s.delete()

