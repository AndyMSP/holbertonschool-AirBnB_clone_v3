#!/usr/bin/python3
"""top level module to define and run app"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import (
    app_views,
    state_views,
    city_views,
    amenity_views,
    user_views,
    place_views,
    review_views
    )
import os

app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)
app.register_blueprint(state_views)
app.register_blueprint(city_views)
app.register_blueprint(amenity_views)
app.register_blueprint(user_views)
app.register_blueprint(place_views)
app.register_blueprint(review_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Response for resource not found"""
    response = jsonify(error='Not found')
    return (response, 404)


@app.errorhandler(400)
def error_400(error):
    """Response for 400 errors"""
    response = jsonify(error=error.description)
    return (response, 400)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = os.getenv('HBNB_API_PORT')
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
