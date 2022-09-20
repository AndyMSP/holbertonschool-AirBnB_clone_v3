#!/usr/bin/python3
"""Module contains views for State objects"""

from api.v1.views import state_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@state_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """returns all states in json format"""
    list_states = []
    states_v = storage.all(State).values()
    for state in states_v:
        list_states.append(state.to_dict())
    response = (jsonify(list_states), 200)
    return (response)


@state_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """return one specific state in json format or 404 if no match"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        response = (jsonify(state.to_dict()), 200)
        return (response)


@state_views.route('/states/<state_id>', methods=['DELETE'],
                    strict_slashes=False)
def del_state(state_id):
    """delete a state or return 404 if state doesn't exist"""
    state=storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state.delete()
        return (jsonify({}), 200)


@state_views.route('/states', methods=['POST'],
                   strict_slashes=False)
def create_state():
    """create a state or abort with 400 if bad data is passed"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    if 'name' not in payload.keys():
        abort(400, 'Missing name')
    state = State(**payload)
    storage.new(state)
    state_d = state.to_dict()
    response = (jsonify(state_d), 201)
    return (response)


@state_views.route('/states/<state_id>', methods=['PUT'],
                   strict_slashes=False)
def update_state(state_id):
    """updates a state"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for k, v in payload.items():
        setattr(state, k, v)
    state.save()
    state_d = state.to_dict()
    response = (jsonify(state_d), 200)
    return (response)