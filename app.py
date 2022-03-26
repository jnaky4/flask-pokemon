from flask import Flask, render_template, request, redirect, url_for, Response
# from flask_cors import CORS, cross_origin
from werkzeug import exceptions
from sqlalchemy import select, create_engine, Column, Integer, String, Float, Table, MetaData, delete, or_
from sqlalchemy.orm import declarative_base, sessionmaker

# Models Imports
# from Models import db
from Models import Base
from Models.PokemonModel import Pokemon
from Models.UserModel import User
from Models.BaseStatModel import Base_Stat

from User.UserFunctions import current_milli_time
from Pokemon.Pokemon import typing_csv_dict, get_all_pokemon_weakness_resistance
from Docker.docker_library import auto_start_container
from Database.database import reset_database

# print(typing_csv_dict["Grass"]["Fire"])
# get_all_pokemon_weakness_resistance("Water", "Psychic")

# print(pokemon_csv_data[25])


"""dotenv lib to load .env file for flask config"""
# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     load_dotenv()


app = Flask(__name__)


# runs the image postgres and creates a container called pokemon-postgres
auto_start_container("postgres", "pokemon-postgres")
reset_database()

# db.init_app(app)

# cors = CORS(app)
# oauth = OAuth(app)
# ma = Marshmallow(app)


# this is cool, specifying type
# Pikachu: Pokemon = createPokemon(25, pokemon_csv_dict)
# print(Pikachu)
# Why is it having issues finding class members
# print(Pikachu.name)


# Connection Explanation:
# Driver :// user : password @ hostname(uri) : port / Database
# engine = create_engine('postgresql://postgres:pokemon@localhost:5432/Pokemon')
engine = create_engine('postgresql://postgres:pokemon@192.168.130.1:5432/Pokemon')
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


# app.register_blueprint(ehandle, url_prefix="")
# app.register_blueprint(authO, url_prefix="")
# app.register_blueprint(home_blueprint, url_prefix="")
# app.register_blueprint(api_endpoints, url_prefix="")

# engine = db.engine
# connection = engine.connect()


@app.route('/')
def main():

    return render_template('main.html')


@app.route('/crm/')
def hello_world():
    raise exceptions.BadRequest
    # return render_template('errorTest.html')


@app.route('/login/')
# @cross_origin()
def login():
    return render_template('login.html')


@app.route('/pokedex')
# @cross_origin()
def pokedex_table():

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
    print(pokemon_dict)

    for b in session.query(Base_Stat).all():
        pokemon_dict[b.dexnum]['Stats'] = b

    return render_template('pokedex_table.html', pokemon_dict=pokemon_dict)


@app.route('/createUser', methods=['GET', 'POST'])
# @cross_origin()
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

        # Example of Delete from database
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


@app.route('/pokedex_grid')
def pokedex_grid():
    pokemon_dict = {}

    if request.args.get('delete'):
        # print(f"Delete: {delete}")
        delete_pokemon = request.args.get("delete")
        print(f"Delete: {delete_pokemon}")
        query = session.query(Pokemon).get(delete_pokemon)
        if query:
            session.delete(query)
            session.commit()
        query = session.query(Base_Stat).get(delete_pokemon)
        if query:
            session.delete(query)
            session.commit()

    # if type passed in as url param, only query pokemon with matching type
    if request.args.get('type'):
        print("TYPE")
        clicked_type = request.args.get('type')
        for p in session.query(Pokemon).filter(or_(Pokemon.type1 == clicked_type, Pokemon.type2 == clicked_type,)):
            pokemon_dict[p.dexnum] = {}
            pokemon_dict[p.dexnum]['Pokemon'] = p
            pokemon_dict[p.dexnum]['Type'] = get_all_pokemon_weakness_resistance(p.type1, p.type2)
            # print(p.dexnum)
            b = session.query(Base_Stat).filter_by(dexnum=p.dexnum)
            for s in b:
                pokemon_dict[p.dexnum]['Stats'] = s
            # print(pokemon_dict[p.dexnum]['Stats'])
        # for b in session.query(Base_Stat).all():
        #     pokemon_dict[b.dexnum]['Stats'] = b

    else:
        for p in session.query(Pokemon).all():
            pokemon_dict[p.dexnum] = {}
            pokemon_dict[p.dexnum]['Pokemon'] = p
            # pokemon_dict[p.dexnum]['Type'] = get_all_pokemon_weakness_resistance(Pokemon.type1, Pokemon.type2)
            pokemon_dict[p.dexnum]['Type'] = get_all_pokemon_weakness_resistance(p.type1, p.type2)
            # print(type)

        for b in session.query(Base_Stat).all():
            pokemon_dict[b.dexnum]['Stats'] = b

    # print(pokemon_dict)
    return render_template('Pokedex_Grid.html', pokemon_dict=pokemon_dict)


@app.route('/1')
def test_route():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
    # app.run(debug=True)

