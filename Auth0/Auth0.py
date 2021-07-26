from flask import Blueprint
from authlib.integrations.flask_client import OAuth, OAuthError

authO = Blueprint('authO', __name__)

