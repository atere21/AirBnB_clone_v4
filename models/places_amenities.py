#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os
import sqlalchemy


db = os.environ.get('HBNB_TYPE_STORAGE', 'jsonfile')


@app_views.route('/places/<place_id>/amenities')
def amenities_from_place(place_id=None):
    """ Show amenities from place
    ---
    tags:
        - Place Amenities
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show amenity
      404:
        description: Resource not found
    """
    amenities = []
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        if db == 'db':
            for amenity in place.amenities:
                amenities.append(amenity.to_dict())
            return jsonify(amenities)
        else:
            jsonify(place.amenities())


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'])
def amenity_review_delete(place_id=None, amenity_id=None):
    """ Delete amenities from a place
    ---
    tags:
        - Place Amenities
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
      - name: amenity_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Amenity delated
      404:
        description: Resource not found
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        abort(404)
    list = [item.id for item in place.amenities]
    if amenity.id not in list:
        abort(404)

    if db == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenities().remove(amenity.id)
    place.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def amenity_from_place_post(place_id, amenity_id):
    """ Create a amenity
    ---
    tags:
        - Place Amenities
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
      - name: amenity_id
        in: path
        type: string
        required: true
    responses:
      201:
        description: Amenity created!
      404:
        description: Resource not found
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        abort(404)
    list = [item.id for item in place.amenities]
    if amenity.id in list:
        return (jsonify(amenity.to_dict()), 200)
    if db is 'db':
        place.amenities.append(amenity)
    else:
        place.amenities.append(amenity.id)
    return (jsonify(amenity.to_dict()), 201)
