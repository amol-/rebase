# -*- coding: utf-8 -*-

import redis
from nose.tools import raises

from rebase import *


class Person(Model):
    __namespace__ = 'dict_person'

    name = Field(String)
    surname = Field(String)
    age = Field(Integer)

class TestDict(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', port=6379)

    def teardown(self):
        assert not self.redis.keys()

    def test_create(self):
        l = Dictionary.new(self.redis, contains=Field(int))
        l.delete()

    def test_insert_pystrings(self):
        l = Dictionary.new(self.redis, contains=Field(str))
        l['hi'] = 'hello'
        l['wo'] = 'world'
        l['du'] = 'dude'
        assert len(l) == 3

        assert l['hi'] == 'hello'
        assert l['wo'] == 'world'
        assert l['du'] == 'dude'

        l.deleteall()

    def test_insert_pyints(self):
        l = Dictionary.new(self.redis, contains=Field(int))
        l['hi'] = 0
        l['wo'] = 1
        l['du'] = 2
        assert len(l) == 3

        assert l['hi'] == 0
        assert l['wo'] == 1
        assert l['du'] == 2

        l.deleteall()

    def test_insert_models(self):
        l = Dictionary.new(self.redis, contains=Field(Person))

        l['george'] = Person.new(self.redis, name='george', surname='labor', age=23)
        l['lucas'] = Person.new(self.redis, name='lucas', surname='subprime', age=48)

        assert l['george'].name == 'george'
        assert l['lucas'].age == 48

        assert len(l) == 2

        l.deleteall()

    def test_insert_list(self):
        l = List.new(self.redis, contains=Field(Person))
        l.append(Person.new(self.redis, name='george', surname='labor', age=23))
        l.append(Person.new(self.redis, name='lucas', surname='subprime', age=48))

        l2 = Dictionary.new(self.redis, contains=Field(List, contains=Field(Person)))
        l2['list'] = l

        assert l2['list'][1].name == 'lucas'

        l2.deleteall()