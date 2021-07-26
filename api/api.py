from flask import Blueprint


api_endpoints = Blueprint('api', __name__, url_prefix='/api')


@api_endpoints.route('/get_data')
def get_data():
    return {'key': 'value'}
