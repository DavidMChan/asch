from flask import Flask, render_template
from flask_restful import Api
import pymongo
import random

from experiments import EXPERIMENT_TYPES  # noqa: F401

from asch.config import Config

from asch.server.resources import PlayAPIResource, UnityTaskAPIResource


# Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.get_or_else('flask', 'SECRET_KEY', str(random.random()))


# Setup database connection
mongo_client = pymongo.MongoClient(Config.get_or_else('database', 'CONNECTION_STRING', None))


# Setup API
api = Api(app)

api.add_resource(PlayAPIResource, '/api/v0/play')
api.add_resource(UnityTaskAPIResource, '/api/v0/unity/task')


@app.route('/')
def index():
    return render_template('index.html')


# Basically, if we don't hit an API call, we'll redirect to the react app
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html')


# Actually run the application
if __name__ == '__main__':
    app.run(port=8080, debug=True)
