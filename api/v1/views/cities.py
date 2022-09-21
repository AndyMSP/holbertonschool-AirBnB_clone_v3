#!/usr/bin/python3
"""Module contains views for city objects"""

from api.v1.views import city_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@city_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
    )
def cities_from_state(state_id):
    """returns all cities from a state in json format"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = []
    cities = state.cities
    for city in cities:
        cities_list.append(city.to_dict())
    response = (jsonify(cities_list), 200)
    return (response)


@city_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """return one specific city in json format or 404 if no match"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        response = (jsonify(city.to_dict()), 200)
        return (response)


@city_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def del_city(city_id):
    """delete a city or return 404 if city doesn't exist"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city.delete()
        return (jsonify({}), 200)


@city_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
    )
def create_city(state_id):
    """create a city or abort with 400 if bad data is passed"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    if 'name' not in payload.keys():
        abort(400, 'Missing name')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    payload.update({'state_id': state_id})
    city = City(**payload)
    storage.new(city)
    city_d = city.to_dict()
    response = (jsonify(city_d), 201)
    return (response)


@city_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_city(city_id):
    """updates a state"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for k, v in payload.items():
        setattr(city, k, v)
    city.save()
    city_d = city.to_dict()
    response = (jsonify(city_d), 200)
    return (response)
