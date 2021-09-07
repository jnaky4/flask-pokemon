from sqlalchemy import Column, Integer, String, Float, Sequence
from Models import db


class User(db.Model):
    # A class using Declarative at a minimum needs a __tablename__ attribute,
    # and at least one Column which is part of a primary key
    __tablename__ = 'Users'
    id = Column(Integer, Sequence('seq_reg_id_70', increment=1, start=1), primary_key=True)
    # some databases require len of stings
    name = Column(String(25))
    email = Column(String(25))
    password = Column(String(25))
    telephone = Column(Integer)
    address = Column(String(125))
    city = Column(String(25))
    state = Column(String(2))
    zipcode = Column(Integer)
    # __init__ where are you?

    # Our User class, as defined using the Declarative system, : from Base in __init__.py
    # has been provided with a constructor (e.g. __init__() method)
    # which automatically accepts keyword names that match the columns we’ve mapped.
    # We are free to define any explicit __init__() method we prefer on our class,
    # which will override the default method provided by Declarative.

    # __repr__ :  special method used to represent a class’s objects as a string.
    def __repr__(self):
        return "<User(id=%d, name='%s', email='%s', password='%s', telephone=%d," \
               "address='%s', city='%s', state='%s', zipcode='%d')>" % \
               (self.id, self.name, self.email, self.password, self.telephone,
                self.address, self.city, self.state, self.zipcode)
