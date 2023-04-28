#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
@app_views.route('/amenities/<amenity_id>')
def amenities(amenity_id=None):
    """ Show Amenity
    ---
    tags:
        - Amenity
    parameters:
      - name: amenity_id
        in: path
        type: string
    responses:
      200:
        description: List of amenities
      404:
        description: Resource not found
    """
    amenities = []
    if amenity_id:
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404, description="Resource not found")
        else:
            return jsonify(amenity.to_dict())
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE', 'PUT'])
def amenity_delete_update(amenity_id=None):
    """ Update  amenity
    ---
    tags:
        - Amenity
    parameters:
      - name: amenity_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Amenity updated!
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        to_update = request.get_json()
        for key, value in to_update.items():
            if (key is not "id" and key is not "created_at" and
                    key is not "updated_at" and key is not "state_id"):
                setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities', methods=['POST'])
def amenity_post():
    """ Create amenity
    ---
    tags:
        - Amenity
    responses:
      201:
        description: Amenity created
      400:
        description: Not a JSON or missing name
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    new = request.get_json()
    new_obj = Amenity(**new)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
