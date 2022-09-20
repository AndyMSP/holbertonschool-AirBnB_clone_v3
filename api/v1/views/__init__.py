#!/usr/bin/python3
"""module to import required blueprints"""


from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
state_view = Blueprint('state_views', __name__, url_prefix='/states')

from api.v1.views.index import *
