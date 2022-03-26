from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
import pandas as pd
from typing import Dict
from Docker.docker_library import auto_start_container
from Database.models import base, Pokemon, Base_Stats, User
import os



# client.containers.run("postgres", detach=True, ports=[5432])


# Manual Command to run a docker container
# docker run --name pokemon-postgres -e POSTGRES_PASSWORD=pokemon -d -p 5432:5432 postgres


# Database URL
"""
can include username, password, hostname, database name as well as optional keyword arguments for additional configuration.
typical form: dialect+driver://username:password@host:port/database
https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
"""

# Local Connection
# in-memory-only SQLite database
# engine = create_engine('sqlite:///:memory:')

# Postgres: Currently Used
# Driver :// user : password @ hostname(uri) : port / Database
engine = create_engine('postgresql://postgres:pokemon@localhost:5432/Pokemon')

# My SQL Example
# engine = create_engine('mysql+pymydsql://root@localhost/mydb')


# grabs route correctly independent of OS routing:
#   Linux/Mac: ..//CSV//Pokemon.csv
#   Windows: ..\\CSV\\Pokemon.csv

cwd = os.getcwd()
pokemon_csv = os.path.join(cwd, 'CSV', "Pokemon.csv")
base_stats_csv = os.path.join(cwd, 'CSV', "Base_Stats.csv")

# explanation of csv reader
# https://www.delftstack.com/howto/python/python-csv-to-dictionary/
pokedex_items = pd.read_csv(pokemon_csv, index_col=0, sep=",", encoding='cp1252')
base_stats_items = pd.read_csv(base_stats_csv, index_col=0, sep=",", encoding='cp1252')
# items = pd.read_csv(pokemon_csv, index_col=0, sep=",")

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html?highlight=transpose#pandas.DataFrame.transpose
# transpose flips the keys to be row 0 instead of column 0
pokemon_csv_dict = pokedex_items.transpose().to_dict(orient='series')
base_stats_dict = base_stats_items.transpose().to_dict(orient='series')


def createPokemon(dexnum: int, pokemon_csv_dict: Dict) -> Pokemon:
    return Pokemon(
        dexnum=dexnum,
        name=pokemon_csv_dict[dexnum]['Pokemon_Name'],
        type1=pokemon_csv_dict[dexnum]['Type1'],
        type2=pokemon_csv_dict[dexnum]['Type2'] if pokemon_csv_dict[dexnum]['Type2'] != "-" else "None",
        stage=pokemon_csv_dict[dexnum]['Stage'],
        evolve_level=int(pokemon_csv_dict[dexnum]['Evolve_Level']),
        gender_ratio=pokemon_csv_dict[dexnum]['Gender_Ratio'],
        height=float(pokemon_csv_dict[dexnum]['Height']),
        weight=float(pokemon_csv_dict[dexnum]['Weight']),
        description=pokemon_csv_dict[dexnum]['Description'],
        category=pokemon_csv_dict[dexnum]['Category'],
        lvl_speed=float(pokemon_csv_dict[dexnum]['Leveling_Speed']),
        base_exp=int(pokemon_csv_dict[dexnum]['Base_Exp']),
        catch_rate=int(pokemon_csv_dict[dexnum]['Catch_Rate']),
    )


def createBaseStats(dexnum: int, base_stats_csv_dict: Dict) -> Base_Stats:
    return Base_Stats(
        dexnum=dexnum,
        hp=int(base_stats_dict[dexnum]['HP']),
        attack=int(base_stats_dict[dexnum]['Attack']),
        defense=int(base_stats_dict[dexnum]['Defense']),
        special_attack=int(base_stats_dict[dexnum]['Sp. Atk']),
        special_defense=int(base_stats_dict[dexnum]['Sp. Def']),
        speed=int(base_stats_dict[dexnum]['Speed']),
    )


"""
The MetaData object contains all of the schema constructs we’ve associated with it. 
It supports a few methods of accessing these table objects, 
such as the sorted_tables accessor which returns a list of each Table object in order of foreign key dependency 
(that is, each table is preceded by all tables which it references):
"""
metadata = MetaData()

def reset_database():
    try:
        print("Dropping all Tables on startup")
        Pokemon.__table__.drop(engine)
        Base_Stats.__table__.drop(engine)
        User.__table__.drop(engine)
    except Exception as e:
        print(f"Failed to Drop all: One or More Tables doesn't exists")

    """
    The usual way to issue CREATE is to use create_all() on the MetaData object. 
    This method will issue queries that first check for the existence of each individual table, 
    and if not found will issue the CREATE statements:
    """
    base.metadata.create_all(engine)

    """
    The ORM’s “handle” to the database is the Session. 
    When we first set up the application, at the same level as our create_engine() statement, 
    we define a Session class which will serve as a factory for new Session objects:
    """
    Session = sessionmaker(bind=engine)
    """
    The below Session is associated with our SQL-enabled Engine, 
    but it hasn’t opened any connections yet. When it’s first used, 
    it retrieves a connection from a pool of connections maintained by the Engine, 
    and holds onto it until we commit all changes and/or close the session object.
    """
    session = Session()

    for i in range(1, 152):
        created_pokemon = createPokemon(i, pokemon_csv_dict)
        session.add(created_pokemon)
        session.commit()
        created_base_stats = createBaseStats(i, base_stats_dict)
        session.add(created_base_stats)
        session.commit()

    query = session.query(Pokemon)
    # get grabs ID of 1
    P1 = query.get(1)
    print(P1)

    query = session.query(Base_Stats)
    B1 = query.get(1)
    print(B1)

    user_count = session.query(Pokemon).count()
    print(f"Pokemon Count Before Delete: {user_count}")

    base_count = session.query(Base_Stats).count()
    print(f"Base Stat Count Before Delete: {base_count}")

    # Id Of 1 no longer exists
    # session.delete(P1)
    # session.commit()
    #
    # user_count = session.query(Pokemon).count()
    # print(f"User Count After Delete: {user_count}")
    #
    #
    # query = session.query(Pokemon)
    # P1 = query.get(2)
    # print(P1)
