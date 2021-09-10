from sqlalchemy import Column, Integer, String, Float
from Models import db


class Pokemon(db.Model):
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

