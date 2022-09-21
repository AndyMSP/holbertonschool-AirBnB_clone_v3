#!/usr/bin/python3
"""Module contains views for Amenity objects"""

from api.v1.views import amenity_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@amenity_views.route(
    '/amenities',
    methods=['GET'],
    strict_slashes=False
    )
def all_amenities():
    """returns all amenities in json format"""
    list_amenities = []
    amenities_v = storage.all(Amenity).values()
    for amenity in amenities_v:
        list_amenities.append(amenity.to_dict())
    response = (jsonify(list_amenities), 200)
    return (response)


@amenity_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False
    )
def one_amenity(amenity_id):
    """return one specific amenity in json format or 404 if no match"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        response = (jsonify(amenity.to_dict()), 200)
        return (response)


@amenity_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def del_amenity(amenity_id):
    """delete an amenity or return 404 if amenity doesn't exist"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        amenity.delete()
        return (jsonify({}), 200)


@amenity_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False
    )
def create_amenity():
    """create an amenity or abort with 400 if bad data is passed"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    if 'name' not in payload.keys():
        abort(400, 'Missing name')
    amenity = Amenity(**payload)
    storage.new(amenity)
    amenity_d = amenity.to_dict()
    response = (jsonify(amenity_d), 201)
    return (response)


@amenity_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_amenity(amenity_id):
    """updates an amenity"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for k, v in payload.items():
        setattr(amenity, k, v)
    amenity.save()
    amenity_d = amenity.to_dict()
    response = (jsonify(amenity_d), 200)
    return (response)
