#!/usr/bin/python3
"""top level module to define and run app"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    try:
        host = os.getenv('HBNB_API_HOST')
    except Exception:
        host = '0.0.0.0'
    try:
        port = os.getenv('HBNB_API_PORT')
    except Exception:
        port = '5000'
    app.run(host=host, port=port, threaded=True)

