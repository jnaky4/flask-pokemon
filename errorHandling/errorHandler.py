from flask import Blueprint, render_template
from authlib.integrations.flask_client import OAuth, OAuthError
from werkzeug import exceptions
import jwt


ehandle = Blueprint('errorHandler', __name__)


@ehandle.errorhandler(exceptions.BadRequest)
def handle_bad_request(e):
    print(e)
    return render_template('redirect.html', e=e)


@ehandle.errorhandler(OAuthError)
def handle_auth0(e):
    print(e)
    return render_template('redirect.html', e=e)


@ehandle.errorhandler(jwt.exceptions.ExpiredSignatureError)
def handle_jwt(e):
    print(e)
    return render_template('redirect.html', e=e)


@ehandle.errorhandler(Exception)
def handle_generic_exception(e):
    print(e)
    return render_template('redirect.html', e=e)


@ehandle.errorhandler(404)
def handle_404():
    print("404 error")
    return render_template('redirect.html', e=404)