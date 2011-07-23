# -*- coding: utf-8 -*-

import redis
from nose.tools import raises

from rebase import *


class Person(Model):
    __namespace__ = 'list_person'

    name = Field(String)
    surname = Field(String)
    age = Field(Integer)

class TestList(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', port=6379)

    def teardown(self):
        assert not self.redis.keys()

    def test_create(self):
        l = List.new(self.redis, contains=Field(int))
        l.delete()

    def test_insert_pystrings(self):
        l = List.new(self.redis, contains=Field(str))
        l.append('hello')
        l.append('world')
        l.append('dude')
        assert len(l) == 3

        assert l[0] == 'hello', l[0]
        assert l[1] == 'world', l[1]
        assert l[2] == 'dude', l[2]

        l.deleteall()

    def test_insert_pyints(self):
        l = List.new(self.redis, contains=Field(int))
        l.append(1)
        l.append(2)
        l.append(3)

        assert len(l) == 3

        assert l[0] == 1
        assert l[1] == 2
        assert l[2] == 3

        l.deleteall()

    def test_insert_models(self):
        l = List.new(self.redis, contains=Field(Person))

        l.append(Person.new(self.redis, name='george', surname='labor', age=23))
        l.append(Person.new(self.redis, name='lucas', surname='subprime', age=48))

        assert l[0].name == 'george'
        assert l[1].age == 48

        assert len(l) == 2

        l.deleteall()

    def test_nested_lists(self):
        l = List.new(self.redis, contains=Field(Person))
        l.append(Person.new(self.redis, name='george', surname='labor', age=23))
        l.append(Person.new(self.redis, name='lucas', surname='subprime', age=48))

        l2 = List.new(self.redis, contains=Field(List, contains=Field(Person)))
        l2.append(l)

        assert l2[0][1].name == 'lucas'

        l2.deleteall()