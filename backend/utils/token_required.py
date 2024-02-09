from functools import wraps
from flask import jsonify, request
from oauthlib.oauth2.rfc6749.errors import InvalidTokenError

from project.backend.auth.controller.auth_controller import AuthController

authController = AuthController()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.cookies.get('token')
            if token is None:
                return jsonify({'error': 'Unauthorised'}), 401
            authController.authentication(token)
            return f(*args, **kwargs)
        except InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 403

    return decorated

def get_user_by_token():
    token = request.cookies.get('token')
    return authController.authentication(token)