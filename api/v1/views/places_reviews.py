#!/usr/bin/python3
"""Module contains views for Review objects"""

from api.v1.views import review_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@review_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False
    )
def reviews_from_place(place_id):
    """returns all reviews from a place in json format"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = []
    reviews = place.reviews
    for review in reviews:
        review_list.append(review.to_dict())
    response = (jsonify(review_list), 200)
    return (response)


@review_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False
    )
def one_review(review_id):
    """return one specific review in json format or 404 if no match"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        response = (jsonify(review.to_dict()), 200)
        return (response)


@review_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def del_review(review_id):
    """delete a review or return 404 if review doesn't exist"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review.delete()
        return (jsonify({}), 200)


@review_views.route(
    'places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
    )
def create_review(place_id):
    """create a review or abort with 400 if bad data is passed"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    payload = request.get_json()
    if 'user_id' not in payload.keys():
        abort(400, 'Missing user_id')
    user_id = payload['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in payload.keys():
        abort(400, 'Missing text')
    payload.update({'place_id': place_id})
    review = Review(**payload)
    storage.new(review)
    review_d = review.to_dict()
    response = (jsonify(review_d), 201)
    return (response)


@review_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_review(review_id):
    """updates a review"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    payload = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for k, v in payload.items():
        setattr(review, k, v)
    review.save()
    review_d = review.to_dict()
    response = (jsonify(review_d), 200)
    return (response)
