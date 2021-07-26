from flask import Flask, render_template, request, redirect, url_for
from werkzeug import exceptions
from authlib.integrations.flask_client import OAuth, OAuthError
# used for catching token exceptions
import jwt
import json
from logging.config import dictConfig

# loads config from .env
from dotenv import load_dotenv, find_dotenv
# used for cross-site pages
from flask_cors import CORS, cross_origin

from errorHandling.errorHandler import ehandle
from Auth0.Auth0 import authO
from home.main_page import home_blueprint
from api.api import api_endpoints

"""dotenv lib to load .env file for flask config"""
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv()


"""Logging config needs to be created before creating the application object"""
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
cors = CORS(app)
oauth = OAuth(app)

app.register_blueprint(ehandle, url_prefix="")
app.register_blueprint(authO, url_prefix="")
app.register_blueprint(home_blueprint, url_prefix="")
app.register_blueprint(api_endpoints, url_prefix="")


@app.route('/crm/')
def hello_world():
    raise exceptions.BadRequest
    # return render_template('errorTest.html')


@app.route('/login/')
@cross_origin()
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)

