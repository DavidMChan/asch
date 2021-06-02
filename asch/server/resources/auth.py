import base64
import jwt
import random

from flask import request
from flask_restful import Resource

from asch.config import Config
from asch.server.auth import User


class LoginAPIResource(Resource):

    def post(self,):
        try:
            username, password = base64.b64decode(
                request.headers['Authorization'].encode('utf8')).decode('utf8').split(':')
        except KeyError:
            return {'error': 'Invalid username / password'}, 403
        active_user = User.get(username)
        if active_user and active_user.validate_password(password):
            return {'token': active_user.get_token()}, 200
        return {'error': 'Invalid username / password'}, 403

class LoginValidateAPIResource(Resource):

    def get(self,):
        try:
            if 'Authorization' in request.headers:
                # Validate the jwt
                data = jwt.decode(request.headers['Authorization'], Config.get_or_else('flask', 'SECRET_KEY', str(random.random())), algorithms=['HS256'])
                user = User.get(data['public_id'])
                if user and user.validate_token(data['token']):
                    return {}, 200
        except jwt.exceptions.DecodeError:
            pass
        return {'error': 'Invalid session token'}
