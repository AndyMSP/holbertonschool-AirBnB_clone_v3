#!/usr/bin/python3
"""Module contains views for State objects"""

from api.v1.views import state_views
from flask import jsonify, abort
from models.state import State
from models import storage


@state_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """returns all states in json format"""
    list_states = []
    states_v = storage.all(State).values()
    for state in states_v:
        list_states.append(state.to_dict())
    states_j = jsonify(list_states)
    return (states_j)


@state_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """return one specific state in json format or 404 if no match"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state_j = jsonify(state.to_dict())
        return (state_j)
