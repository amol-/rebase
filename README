Rebase wannabe Redis ORM
-----------------------------

Rebase is a wannabe Redis ORM for Python::

    import redis
    from rebase import *

    class Person(Model):
        __namespace__ = 'person'

        name = Field(String)
        surname = Field(String)
        age = Field(Integer)
        mother = Field(Reference, contains=Field('Person'))
        father = Field(Reference, contains=Field('Person'))
        children = Field(List, contains=Field('Person'))


    redis = redis.Redis('localhost', port=6379)


    def create_things():
        m = Person.new(redis, name='Arianne', surname='Doe', age=67,
                              children=List.new(redis, contains=Field(Person)))
        f = Person.new(redis, name='Marcus', surname='Doe', age=71,
                              children=List.new(redis, contains=Field(Person)))
        p = Person.new(redis, name='John', surname='Doe', age=38, mother=m, father=f)

        m.children.append(p)
        f.children.append(f)

        return p.redis_key

    def load_back(key):
        p = Person.get(redis, key)

        print p.name, p.surname
        print 'Son of', p.mother.name, p.mother.surname, 'and', p.father.name, p.father.surname
        print 'Siblings', ['{c.name} {c.surname}'.format(c=c) for c in p.mother.children]

    load_back(create_things())

    redis.flushall()


