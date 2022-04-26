import random

import pymongo
from flask import Flask, render_template
from flask_restful import Api

from asch.config import Config
from asch.server.resources import *
from experiments import EXPERIMENT_TYPES  # noqa: F401

# Flask app configuration
app = Flask(__name__, static_url_path='/')
app.config['SECRET_KEY'] = Config.get_or_else('flask', 'SECRET_KEY', str(random.random()))

# Setup database connection
mongo_client = pymongo.MongoClient(Config.get_or_else('database', 'CONNECTION_STRING', None))

# Setup API
api = Api(app)

api.add_resource(PlayAPIResource, '/api/v0/play')
api.add_resource(UnityTaskAPIResource, '/api/v0/unity/task')
api.add_resource(ParticipantViewAPIResource, '/api/v0/participants')
api.add_resource(ParticipantFinishedAPIResource, '/api/v0/particpants/finished')
api.add_resource(DownloadParticipantDataAPIResource, '/api/v0/data/download')
api.add_resource(LoginAPIResource, '/api/v0/login')
api.add_resource(LoginValidateAPIResource, '/api/v0/validate_session')


@app.route('/')
def index():
    return app.send_static_file('index.html')


# Basically, if we don't hit an API call, we'll redirect to the react app
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


# Actually run the application
if __name__ == '__main__':

    app.run(port=8080, debug=True)
