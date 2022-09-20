#!/usr/bin/python3
"""module to define blueprint"""

from api.v1.views import app_views
from flask import jsonify
import json


@app_views.route('/status')
def status():
    """returns status in json format"""
    response = jsonify(status='OK')
    return(response)
