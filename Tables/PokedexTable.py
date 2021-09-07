from sqlalchemy import Column, Integer, String, Float, Table
from Tables import metadata


"""
Below, a table called Pokemon is described, which contains 14 columns. 
The primary key of the table consists of the dexnum column. 
Multiple columns may be assigned the primary_key=True flag which denotes a multi-column primary key, 
known as a composite primary key.
"""


Pokedex_table = Table('Pokedex', metadata,
    Column('dexnum', Integer, primary_key=True),
    Column('name', String(11), nullable=False),
    Column('type1', String(10), nullable=False),
    Column('type2', String(10), nullable=True),
    Column('stage', String(12), nullable=False),
    Column('evolve_level', Integer, nullable=False),
    Column('gender_ratio', String(5), nullable=False),
    Column('height', Float(3), nullable=False),
    Column('weight', Float(3), nullable=False),
    Column('description', String(125), nullable=False),
    Column('category', String(20), nullable=False),
    Column('lvl_speed', Float(3), nullable=False),
    Column('base_exp', Integer, nullable=False),
    Column('catch_rate', Integer, nullable=False)
                      )
