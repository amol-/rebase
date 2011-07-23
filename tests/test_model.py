# -*- coding: utf-8 -*-

import redis
from nose.tools import raises

from rebase import *



class Person(Model):
    __namespace__ = 'person'

    name = Field(String)
    surname = Field(String)
    age = Field(Integer)
    mother = Field(Reference, contains=Field('Person'))
    father = Field(Reference, contains=Field('Person'))
    children = Field(List, contains=Field('Person'))

class Application(Model):
    __namespace__ = 'application_data'

    people = Field(List, contains=Field(Person))
    options = Field(Dictionary, contains=Field(str))
    groups = Field(Dictionary, contains=Field(List, contains=Field(Person)))

class TestModel(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', port=6379)

    def teardown(self):
        assert not self.redis.keys()

    def test_create(self):
        o = Person.new(self.redis, name='John', surname='Doe', age=38)
        assert o.name == 'John', o.name.__class__
        assert o.surname == 'Doe', o.surname
        assert o.age == 38, o.age
        o.delete()


    def test_save_restore(self):
        o = Person.new(self.redis, name='John', surname='Doe', age=38)
        x = Person.get(self.redis, o._key)
        assert x.name == 'John', o.name
        assert x.surname == 'Doe', o.surname
        assert x.age == 38, o.age
        o.delete()
        x.delete()

    def test_references(self):
        m = Person.new(self.redis, name='Arianne', surname='Doe', age=67)
        f = Person.new(self.redis, name='Marcus', surname='Doe', age=71)
        o = Person.new(self.redis, name='John', surname='Doe', age=38, mother=m, father=f)

        assert o.mother.name == 'Arianne'
        assert o.father.name == 'Marcus'

        m.delete()
        f.delete()

        assert o.mother is None
        assert o.father is None
        o.delete()

    def test_list_references(self):
        o = Person.new(self.redis, name='John', surname='Doe', age=38)
        c1 = Person.new(self.redis, name='John Jr.', surname='Doe')
        c2 = Person.new(self.redis, name='Anthony', surname='Doe')

        o.children.append(c1)
        o.children.append(c2)

        assert len(o.children) == 2
        assert o.children[0].name == 'John Jr.'
        assert o.children[1].name == 'Anthony'

        c1.delete()
        c2.delete()

        assert len(o.children) == 2
        assert not o.children[0]

        o.delete()

    def test_complex_model(self):
        m = Application.new(self.redis)
        m.people.append(Person.new(self.redis, name='John', surname='Doe', age=38))
        m.people.append(Person.new(self.redis, name='John2', surname='Doe', age=38))
        m.people.append(Person.new(self.redis, name='John3', surname='Doe', age=38))

        m.options['people'] = len(m.people)

        m.groups['admins'] = List.new(self.redis, contains=Field(Person))
        m.groups['admins'].append(m.people[0])

        m.groups['users'] = List.new(self.redis, contains=Field(Person))
        m.groups['users'].append(m.people[1])
        m.groups['users'].append(m.people[2])

        m.groups.deleteall()
        m.people.deleteall()
        m.options.deleteall()
        m.delete()