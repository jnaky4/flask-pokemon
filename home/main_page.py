from flask import Blueprint, render_template
from authlib.integrations.flask_client import OAuth, OAuthError


home_blueprint = Blueprint('home_blueprint', __name__, static_folder="static", template_folder="template")


@home_blueprint.route('/')
# @home_blueprint.route('/home')
def render_page():
    return render_template('login.html')

