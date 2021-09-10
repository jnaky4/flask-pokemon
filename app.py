from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, redirect, render_template, session, url_for, Response, request

from werkzeug import exceptions

from authlib.integrations.flask_client import OAuth, OAuthError
# used for catching token exceptions

from logging.config import dictConfig
# loads config from .env
from dotenv import load_dotenv, find_dotenv
# used for cross-site pages


# from Models import Base
from errorHandling.errorHandler import ehandle
from Auth0.Auth0 import authO
from home.main_page import home_blueprint
from api.api import api_endpoints
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import select, create_engine, Column, Integer, String, Float, Table, MetaData, delete
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.sql import func

from datetime import datetime, timedelta
from typing import Dict, List
import pprint
import jwt
import json
import time

from Pokemon.Pokemon import pokemon_csv_dict, createPokemon


# Models Imports
# from Models import db
from Models import Base
from Models.PokemonModel import Pokemon
from Models.UserModel import User
from Models.BaseStatModel import Base_Stat

# Tables Imports Not needed
from Tables import metadata
from Tables.PokedexTable import Pokedex_table
from Tables.UserTable import UserTable
from User.UserFunctions import userExist

from User.UserFunctions import current_milli_time

# print(pokemon_csv_data[25])


"""dotenv lib to load .env file for flask config"""
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv()




app = Flask(__name__)

# Database URL
"""
can include username, password, hostname, database name as well as optional keyword arguments for additional configuration.
typical form: dialect+driver://username:password@host:port/database
https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
"""


""""""

# db.init_app(app)



# cors = CORS(app)
# oauth = OAuth(app)
# ma = Marshmallow(app)


# this is cool, specifying type
# Pikachu: Pokemon = createPokemon(25, pokemon_csv_dict)
# print(Pikachu)
# Why is it having issues finding class members
# print(Pikachu.name)




# Local Connection
# in-memory-only SQLite database
"""
The Engine, when first returned by create_engine(), 
has not actually tried to connect to the database yet; 
that happens only the first time it is asked to perform a task against the database.
"""
# engine = create_engine('sqlite:///:memory:', echo=True)
# Todo figure out correct way, without using check_same_thread
# engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
# engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})

engine = create_engine('postgresql://postgres:pokemon@localhost:5432/Pokemon')


"""
The MetaData object contains all of the schema constructs we’ve associated with it. 
It supports a few methods of accessing these table objects, 
such as the sorted_tables accessor which returns a list of each Table object in order of foreign key dependency 
(that is, each table is preceded by all tables which it references):
"""

# print("here")
for table in metadata.sorted_tables:
    print(f"tablename: {table.name}")


"""
The usual way to issue CREATE is to use create_all() on the MetaData object. 
This method will issue queries that first check for the existence of each individual table, 
and if not found will issue the CREATE statements:
"""

Base.metadata.create_all(engine)

"""
The ORM’s “handle” to the database is the Session. 
When we first set up the application, at the same level as our create_engine() statement, 
we define a Session class which will serve as a factory for new Session objects:
"""
Session = sessionmaker(bind=engine)
"""
The below Session is associated with our SQLite-enabled Engine, 
but it hasn’t opened any connections yet. When it’s first used, 
it retrieves a connection from a pool of connections maintained by the Engine, 
and holds onto it until we commit all changes and/or close the session object.
"""
session = Session()




# for i in range(1, 152):
#     created_pokemon = createPokemon(i, pokemon_csv_dict)
#     session.add(created_pokemon)
#     session.commit()
#
# pokemon_count = session.query(Pokemon).count()
# print(f"pokemon_count: {pokemon_count}")
#
#
# pokemon_query = session.query(Pokemon).filter(Pokemon.name.ilike("Pi%"))
# print(f"""
#     First Object: {pokemon_query.first()}
#
#         """
#     )



app.register_blueprint(ehandle, url_prefix="")
app.register_blueprint(authO, url_prefix="")
# app.register_blueprint(home_blueprint, url_prefix="")
app.register_blueprint(api_endpoints, url_prefix="")

# engine = db.engine
# connection = engine.connect()


@app.route('/crm/')
def hello_world():
    raise exceptions.BadRequest
    # return render_template('errorTest.html')


@app.route('/login/')
@cross_origin()
def login():
    return render_template('login.html')


@app.route('/pokedex')
@cross_origin()
def data_visuals():
    if len(request.args) > 0:
        dexnum = request.args.get("dexnum")
        print(f"Dexnum: {dexnum}")
        query = session.query(Pokemon).get(dexnum)
        if query:
            session.delete(query)
            session.commit()
        query = session.query(Base_Stat).get(dexnum)
        if query:
            session.delete(query)
            session.commit()

    pokemon_dict = {}

    for p in session.query(Pokemon).all():
        pokemon_dict[p.dexnum] = {}
        pokemon_dict[p.dexnum]['Pokemon'] = p

    for b in session.query(Base_Stat).all():
        pokemon_dict[b.dexnum]['Stats'] = b


    return render_template('pokedex_table.html', pokemon_dict=pokemon_dict)


@app.route('/createUser', methods=['GET', 'POST'])
@cross_origin()
def create_user():
    if request.form:
        print(f"""
            User Added!
            name: {request.form['first name'] + " " + request.form['last name']}
            email: {request.form['email']}
            password: {request.form['password']}
            telephone: {int(request.form['tel'])}
            address: {request.form['address1'] + " " + request.form['address2']}
            city: {request.form['city']}
            state: {request.form['state']}
            zip_code: {int(request.form['zip code'])}             
            """
              )

        print(f"time: {current_milli_time()%1000000000}")
        session.add(User(
            name=request.form['first name'] + " " + request.form['last name'],
            email=request.form['email'],
            password=request.form['password'],
            telephone=request.form['tel'],
            address=request.form['address1'] + " " + request.form['address2'],
            city=request.form['city'],
            state=request.form['state'],
            zipcode=int(request.form['zip code'])
        ))

        session.commit()

        user_count = session.query(User).count()
        print(f"User Count: {user_count}")

        #
        # user_query = session.query(User).filter(User.name.ilike(request.form['first name'] + "%"))
        # print(user_query.first())
        # # session.delete(User(id=1))
        #
        # user_count = session.query(User).count()
        # print(f"User Count: {user_count}")
        #
        # # session.commit()
        #
        # user_count = session.query(User).count()
        # print(f"User Count: {user_count}")

    return render_template('createUser.html')


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
