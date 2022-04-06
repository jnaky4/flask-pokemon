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

    # Our Pokemon class, as defined using the Declarative system, : from Base in __init__.py
    # has been provided with a constructor (e.g. __init__() method)
    # which automatically accepts keyword names that match the columns we’ve mapped.
    # We are free to define any explicit __init__() method we prefer on our class,
    # which will override the default method provided by Declarative.

    # __repr__ :  special method used to represent a class’s objects as a string.
    def __repr__(self):
        return f"<Pokemon(dexnum={self.dexnum}, name='{self.name}', type1='{self.type1}', type2='{self.type2}', " \
               f"evolve_level={self.evolve_level}, gender_ratio='{self.gender_ratio}', height={self.height}, " \
               f"weight={self.weight}, category='{self.category}', lvl_speed={self.lvl_speed}, " \
               f"base_exp={self.base_exp}, catch_rate={self.catch_rate}" \
               f"description='{self.description}')>"


# class Route(base):
#     __tablename__ = 'Routes'
#     area = Column(String, primary_key=True)
#     available_pokemon = Column([])
#
#
# class Available(base):
#
#     pass


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
        return f"<Base_Stats(dexnum={self.dexnum}, hp={self.hp}, attack={self.attack}, defense={self.defense}," \
               f"special_attack={self.special_attack}, special_defense={self.defense}, speed={self.speed})>"



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
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', password='{self.password}', telephone='{self.telephone}'," \
               f"address='{self.address}'," \
               f"city='{self.city}', state='{self.state}', zipcode={self.zipcode})>"
