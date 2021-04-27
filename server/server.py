from flask import Flask, render_template
from flask_restful import Api
import pymongo

FLASK_SECRET_KEY = 'Hello World'

# Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Setup API and JWT
api = Api(app)


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
