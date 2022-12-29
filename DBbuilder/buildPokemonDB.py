from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
import pandas as pd
import os
import docker
from docker.errors import APIError, NotFound
import time
from typing import Optional, Dict

docker_client = docker.DockerClient('unix:///Users/Z004X7X/.colima/default/docker.sock')

# docker_client.containers.run("postgres", detach=True, ports=[5432])


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
pokemon_csv = os.path.join(cwd, "Pokemon.csv")
base_stats_csv = os.path.join(cwd, "Base_Stats.csv")
routes_csv = os.path.join(cwd, "Routes.csv")


# explanation of csv reader
# https://www.delftstack.com/howto/python/python-csv-to-dictionary/
pokedex_items = pd.read_csv(pokemon_csv, index_col=0, sep=",", encoding='cp1252')
base_stats_items = pd.read_csv(base_stats_csv, index_col=0, sep=",", encoding='cp1252')
route_item = pd.read_csv(routes_csv, index_col=0, sep=",", encoding='cp1252')
# items = pd.read_csv(pokemon_csv, index_col=0, sep=",")


# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html?highlight=transpose#pandas.DataFrame.transpose
# transpose flips the keys to be row 0 instead of column 0
pokemon_csv_dict = pokedex_items.transpose().to_dict(orient='series')
base_stats_dict = base_stats_items.transpose().to_dict(orient='series')
# route_dict = route_item.transpose().to_dict(orient='series')




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


# print(route_dict)
def create_route_dict(route_list):
    for i in route_item:
        print(route_item)
    pass


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


def create_postgres_container(container_name: str, image_name: str, timeout: int = 30):
    """
    image (str) – The image to run.
    name (str) – The name for this container.
    ports (dict) –
        Ports to bind inside the container.
        The keys of the dictionary are the ports to bind inside the container,
        either as an integer or a string in the form port/protocol,
        where the protocol is either tcp, udp, or sctp.

        The values of the dictionary are the corresponding ports
        to open on the host, which can be either:

            The port number, as an integer. For example:
                {'2222/tcp': 3333} will expose port 2222 inside the container as port 3333 on the host.

            None, to assign a random host port. For example:
                {'2222/tcp': None}.
            A tuple of (address, port) if you want to specify the host interface. For example:
                {'1111/tcp': ('127.0.0.1', 1111)}.
            A list of integers, if you want to bind multiple host ports to a single container port. For example:
                {'1111/tcp': [1234, 4567]}.
        Incompatible with host network mode.

    Postgres Environment Variables:
    https://github.com/docker-library/docs/tree/master/postgres
    POSTGRES_DB
        This optional environment variable can be used to define a different name for the default database that
        is created when the image is first started. If it is not specified, then the value of POSTGRES_USER will
        be used.

    POSTGRES_PASSWORD
        This environment variable is required for you to use the PostgreSQL image. It must not be
        empty or undefined. This environment variable sets the superuser password for PostgreSQL.
        The default superuser is defined by the POSTGRES_USER environment variable.
    """
    container = docker_client.containers.run(
        image_name,
        detach=True,
        name=container_name,
        ports={'5432/tcp': 5432},
        environment={"POSTGRES_PASSWORD": "pokemon", "POSTGRES_DB": "Pokemon"}
    )

    """
    Similar to the pg_isready command: https://www.postgresql.org/docs/9.3/app-pg-isready.html
    waits until the server is accepting connections
    """

    current_time = 0
    exit_code = -2
    while exit_code != 0 and current_time != timeout:
        returned = container.exec_run(f"pg_isready")
        print(f"pg_isready: {returned}")
        if len(returned) > 0:
            exit_code = returned[0]
        time.sleep(1)
        current_time += 1

    print(f"Container {container} Ready")

def auto_start_container(image_name: str, container_name: str):
    # How many seconds we are willing to wait for container to run
    timeout = 10

    # does container exists on system
    container_already_exists = container_exists(container_name)

    if container_already_exists:
        # is container running already?
        container_running = is_container_running(container_name)
        # container is already running on system, do we want to restart container? or do nothing?
        if container_running:
            print(f"Container Already Running: {container_name}")
            return
        # container isn't running, run container
        else:
            start_container(container_name)

    # container doesnt exist, check if image exists
    else:
        print(f"Image Name: {image_name}")
        does_image_exist = image_exists(image_name)
        print(f"exists: {does_image_exist}")
        if not does_image_exist:
            print(f"Pulling Image {image_name}, may take a minute")
            image_id = pull_image(image_name)
            if image_id is None:
                print("Image does not exist as a repository to pull from, try another name")
                return
        try:
            if image_name == "postgres":
                create_postgres_container(container_name, image_name, timeout)
        except Exception as e:
            print(f"Exception: {e}")


def image_exists(image_name: str) -> Optional[bool]:
    try:
        """
        get(name)
        Gets an image.

        Parameters:	
        name (str) – The name of the image.

        Returns:	
        The image.

        Return type:	
        (Image)

        Raises:	
        docker.errors.ImageNotFound – If the image does not exist.
        docker.errors.APIError – If the server returns an error.

        """
        image = docker_client.images.get(image_name)
        print(f"Image {image_name} Exists: {image.id}")
        return True
    except NotFound as e:
        print(f"Image Doesn't Exists: Error Generated: {e}")
    except Exception as e:
        print(f"Exception: {e}")
    return False


def start_container(container_name: str):
    print(f"Starting Container: {container_name}")

    existing_container = docker_client.containers.get(container_name)
    # print(f"Existing Container {existing_container}")
    try:
        existing_container.start()

    except APIError:
        print(f"{container_name} failed")

    print(f"Container {container_name} started")


def pull_image(image_name: str) -> Optional[str]:
    try:
        image = docker_client.images.pull(image_name)
        print(f"Pulled Image {image_name}, id:{image.id}")
        return image.id
    except Exception as e:
        print(f"Exception: {e}")
        return None


def container_exists(container_name: Optional[str] = None, container_id: Optional[str] = None) -> Optional[bool]:
    if container_name is None and container_id is None:
        print("Please pass in an Id or name")
        return False

    exists = False

    identification = container_name if container_id is None else container_id
    try:
        container = docker_client.containers.get(identification)
        # print(f"Container {identification} Exists ID: {container.id}")
        print(f"Container {identification} Exists,\nID: {container.id}")
        return True
    except NotFound as e:
        print(f"Container Doesn't Exists: Error Generated: {e}")
    except Exception as e:
        print(f"Exception: {e}")
    return exists


def is_container_running(container_name: str) -> Optional[bool]:
    container_running = False
    try:
        """
        To talk to a Docker daemon, you first need to instantiate a client.
        You can use from_env() to connect using the default socket or the configuration in your environment:
        """
        # Grab the container by name

        docker_container = docker_client.containers.get(container_name)

        # get the state of the container
        container_state = docker_container.attrs['State']
        # print(f"container state: {container_state['Status']}")
        container_running = container_state['Status'] == 'running'
        # print(f"Container Status: {container_state['Status']}")
        print(f"Container Running: {container_running}")
    except NotFound as e:
        print(f"Container Doesn't Exists")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        return container_running


if __name__ == "__main__":
    auto_start_container("postgres", "pokemon-postgres")
    reset_database()
