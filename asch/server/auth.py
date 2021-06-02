import datetime
import hashlib
import random
import secrets
from functools import wraps
from typing import Any, Dict, List

import jwt
import pymongo
from flask import request

from asch.config import Config


class User():

    _db = pymongo.MongoClient(Config.get_or_else('database', 'CONNECTION_STRING', None)).asch

    def __init__(self, _id=None, username=None, password_hash=None, salt=None, tokens=None):

        self._id = _id
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.tokens = tokens

    def todict(self,) -> Dict[str, Any]:
        output = {
            'username': self.username,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'tokens': self.tokens
        }
        if self._id is not None:
            output.update({'_id': self._id})
        return output

    def validate_password(self, password: str) -> bool:
        return hashlib.sha512((password + self.salt or '').encode('utf8')).hexdigest() == self.password_hash

    def validate_token(self, token: str) -> bool:
        if token in (self.tokens or {}):
            token_expiry = datetime.datetime.strptime(self.tokens[token], "%Y-%m-%dT%H:%M:%S.%f")
            if token_expiry > datetime.datetime.utcnow():
                return True
        return False

    def get_token(self, expiry=None) -> str:
        if self.tokens is not None:
            for k, v in self.tokens.items():
                token_expiry = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                if token_expiry > datetime.datetime.utcnow():
                    return jwt.encode({
                        'public_id': self.username,
                        'token': k
                    }, Config.get_or_else('flask', 'SECRET_KEY', str(random.random())))

        # Generate a token
        if expiry is None:
            expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat()
        self.tokens = {}
        token = secrets.token_hex(64)
        self.tokens[token] = expiry

        User.update(self)

        return token

    @classmethod
    def fromdict(cls, input_dict) -> 'User':
        return User(**input_dict)

    @classmethod
    def fetch_all(cls, filter) -> List['User']:
        return [cls.fromdict(u) for u in cls._db.users.find(filter)]

    @classmethod
    def get(cls, username) -> 'User':
        u = cls._db.users.find_one({'username': username})
        if u is None:
            return None
        return cls.fromdict(u)

    @classmethod
    def update(cls, user: 'user') -> 'user':
        cls._db.users.replace_one({'_id': user._id}, user.todict())
        return True


def protected(f):

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return {'message': 'a valid token is missing'}, 403

        # try:
        data = jwt.decode(token, Config.get_or_else('flask', 'SECRET_KEY', str(random.random())), algorithms=['HS256'])
        user = User.get(data['public_id'])
        if user and user.validate_token(data['token']):
            return f(user, *args, **kwargs)
        # except:
        #     return {'message': 'a valid token is missing'}, 403

        return {'message': 'a valid token is missing'}, 403

    return decorator
