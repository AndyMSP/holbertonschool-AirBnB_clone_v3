#!/usr/bin/python3
"""module to define blueprint"""

from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status():
    """returns status in json format"""
    response = jsonify(status='OK')
    return(response)


@app_views.route('/stats')
def stats():
    """returns count of each object in storage"""
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    response = jsonify(amenities=storage.count(Amenity),
                       cities=storage.count(City),
                       places=storage.count(Place),
                       reviews=storage.count(Review),
                       states=storage.count(State),
                       users=storage.count(User))
    return (response)
