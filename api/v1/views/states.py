#!/usr/bin/python3
"""Module contains views for State objects"""

from api.v1.views import state_views
from flask import jsonify
from models.state import State
from models import storage


# @state_views.route('/states', strict_slashes=False)
# def all_states():
#     """returns all states in json format"""
#     list_states = []
#     states_v = storage.all(State).values()
#     for state in states_v:
#         list_states.append(state.to_dict())
#     states_j = jsonify(list_states)
#     return (states_j)
