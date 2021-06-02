import base64

import bson
import pymongo
from flask import Response, request
from flask_restful import Resource

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
            return active_user.get_token()
        return {'error': 'Invalid username / password'}, 403

        # try:

        #     # Get login info from the post data, and then return a token if validation is OK.
        #     active_user = User.get(username)
        #     if active_user or active_user.validate_password(password):
        #         return {'OK'}, 200
        #         # return user.get_token()
        # except:
        #     return {'error', 'Invalid username / password'}, 403
        # return {'error', 'Invalid username / password'}, 403
