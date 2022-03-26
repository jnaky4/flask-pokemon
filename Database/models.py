from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

"""
The Engine, when first returned by create_engine(), 
has not actually tried to connect to the database yet; 
that happens only the first time it is asked to perform a task against the database.
"""
base = declarative_base()


class Pokemon(base):
    # A class using Declarative at a minimum needs a __tablename__ attribute,
    # and at least one Column which is part of a primary key
    __tablename__ = 'Pokedex'
    dexnum = Column(Integer, primary_key=True)
    # some databases require len of stings
    name = Column(String(11), nullable=False)
    type1 = Column(String(10), nullable=False)
    type2 = Column(String(10), nullable=True)
    stage = Column(String(12))
    evolve_level = Column(Integer)
    gender_ratio = Column(String(10))
    height = Column(Float(3))
    weight = Column(Float(3))
    description = Column(String(125))
    category = Column(String(20))
    lvl_speed = Column(Float(3))
    base_exp = Column(Integer)
    catch_rate = Column(Integer)

    # child = relationship("Child", back_populates="Parent", uselist=False)

    # __init__ where are you?

    # Our User class, as defined using the Declarative system, : from Base in __init__.py
    # has been provided with a constructor (e.g. __init__() method)
    # which automatically accepts keyword names that match the columns we’ve mapped.
    # We are free to define any explicit __init__() method we prefer on our class,
    # which will override the default method provided by Declarative.

    # __repr__ :  special method used to represent a class’s objects as a string.
    def __repr__(self):
        return "<Pokemon(dexnum=%d, name='%s', type1='%s', type2='%s', evolve_level=%d," \
               "gender_ratio='%s', height=%f, weight=%f, category='%s'," \
               "lvl_speed=%f, base_exp=%d, catch_rate=%d" \
               "description='%s')>" % \
               (self.dexnum, self.name, self.type1, self.type2, self.evolve_level,
                self.gender_ratio, self.height, self.weight, self.category, self.lvl_speed,
                self.base_exp, self.catch_rate, self.description)


class Base_Stats(base):
    __tablename__ = 'Stats'
    dexnum = Column(Integer, primary_key=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    # total = Column(Integer)
    # dexnum = Column(Integer, ForeignKey(Pokemon.dexnum), primary_key=True)

    # parent = relationship("Parent", backref=backref("child", uselist=False))

    def __repr__(self):
        return "<Base_Stats(dexnum=%d, hp=%d, attack=%d, defense=%d," \
               "special_attack=%d, special_defense=%d, speed=%d)>" % \
               (self.dexnum, self.hp, self.attack, self.defense, self.special_attack,
                self.special_defense, self.speed)


class User(base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(25))
    password = Column(String(25))
    telephone = Column(String(10))
    address = Column(String(250))
    city = Column(String(25))
    state = Column(String(25))
    zipcode = Column(Integer)

    def __repr__(self):
        return "<User(id=%d, name='%s', email='%s', password='%s', telephone='%s'," \
               "address='%s'," \
               "city='%s', state='%s', zipcode=%d)>" % \
               (self.id, self.name, self.email, self.password, self.telephone,
                self.address, self.city, self.state, self.zipcode)