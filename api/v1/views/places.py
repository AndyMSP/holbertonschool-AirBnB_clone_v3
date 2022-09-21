#!/usr/bin/python3
"""Module contains views for place objects"""

from api.v1.views import place_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@place_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False
    )
def places_from_city(city_id):
    """returns all places from a city in json format"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    places = city.places
    for place in places:
        places_list.append(place.to_dict())
    response = (jsonify(places_list), 200)
    return (response)


@place_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """return one specific place in json format or 404 if no match"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        response = (jsonify(place.to_dict()), 200)
        return (response)


@place_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def del_place(place_id):
    """delete a place or return 404 if place doesn't exist"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        place.delete()
        return (jsonify({}), 200)


@place_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
    )
def create_place(city_id):
    """create a place or abort with 400 if bad data is passed"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    if 'user_id' not in payload.keys():
        abort(400, 'Missing user_id')
    user_id = payload['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if 'name' not in payload.keys():
        abort(400, 'Missing name')
    payload.update({'city_id': city_id})
    place = Place(**payload)
    storage.new(place)
    place_d = place.to_dict()
    response = (jsonify(place_d), 201)
    return (response)


@place_views.route(
    '/places/<place_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_place(place_id):
    """updates a place"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for k, v in payload.items():
        setattr(place, k, v)
    place.save()
    place_d = place.to_dict()
    response = (jsonify(place_d), 200)
    return (response)
