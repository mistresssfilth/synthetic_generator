from flask import jsonify, Blueprint, make_response, request

from project.backend.auth.controller.auth_controller import AuthController
from project.backend.exceptions.exceptions import InvalidCredentialsException, AlreadyExistException
from project.backend.utils import token_required
from project.backend.utils.token_required import token_required, get_user_by_token

AUTH_REQUEST_API = Blueprint('request_auth_api', __name__)

authController = AuthController()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return AUTH_REQUEST_API


class AlreadyExistsException:
    pass


@AUTH_REQUEST_API.route('/')
def hello():
    return 'Hello, World!'


@AUTH_REQUEST_API.route('/signup', methods=['POST'])
def registration():
    request_data = request.get_json()
    try:
        email = request_data['email']
        password = request_data['password']
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400
    try:
        authController.register(email, password)
    except AlreadyExistException:
        return jsonify({'error': 'Email already exists'}), 403
    return jsonify({}), 200


@AUTH_REQUEST_API.route('/login', methods=['PUT'])
def login():
    request_data = request.get_json()
    try:
        email = request_data['email']
        password = request_data['password']
    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400
    try:
        token = authController.login(email, password)
        response = make_response()
        response.set_cookie('token', token)
        return response
    except InvalidCredentialsException:
        return jsonify({'error': 'Invalid email or password'}), 403


@AUTH_REQUEST_API.route('/logout', methods=['GET'])
def logout():
    response = make_response()
    response.delete_cookie('token')
    return response


@AUTH_REQUEST_API.route('/profile', methods=['GET'])
@token_required
def get_user_list():
    user = get_user_by_token()

    return jsonify(
        {
            "id": user.get_id(),
            "email": user.email
        }
    ), 200
