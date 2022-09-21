#!/usr/bin/python3
"""Module contains views for User objects"""

from api.v1.views import user_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@user_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """returns all users in json format"""
    list_users = []
    users_v = storage.all(User).values()
    for user in users_v:
        list_users.append(user.to_dict())
    response = (jsonify(list_users), 200)
    return (response)


@user_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def one_user(user_id):
    """return one specific user in json format or 404 if no match"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        response = (jsonify(user.to_dict()), 200)
        return (response)


@user_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def del_user(user_id):
    """delete a user or return 404 if user doesn't exist"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        user.delete()
        return (jsonify({}), 200)


@user_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False
    )
def create_user():
    """create a user or abort with 400 if bad data is passed"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    if 'email' not in payload.keys():
        abort(400, 'Missing email')
    if 'password' not in payload.keys():
        abort(400, 'Missing password')
    user = User(**payload)
    storage.new(user)
    user_d = user.to_dict()
    response = (jsonify(user_d), 201)
    return (response)


@user_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_user(user_id):
    """updates a user"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for k, v in payload.items():
        setattr(user, k, v)
    user.save()
    user_d = user.to_dict()
    response = (jsonify(user_d), 200)
    return (response)
