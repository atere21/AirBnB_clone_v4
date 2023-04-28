#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/cities/<id>')
def cities(id=None):
    """ Show City
    ---
    tags:
        - City
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
        200:
            description: City
        404:
            description: Resource not found
    """
    city = storage.get("City", id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities')
def state_city(id=None, state_id=None):
    """ List of cities by state
    ---
    tags:
        - City
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
    responses:
        200:
            description: List of cities
        404:
            description: Resource not found
    """
    cities = []
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['DELETE', 'PUT'])
def city_delete(city_id=None):
    """ Update City
    ---
    tags:
        - City
    parameters:
      - name: city_id
        in: path
        type: string
        required: true
    responses:
        200:
            description: City updated!
        404:
            description: Resource not found
        400:
            description: Not a JSON
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        to_update = request.get_json()
        for key, value in to_update.items():
            if (key is not "id" and key is not "created_at" and
                    key is not "updated_at" and key is not "state_id"):
                setattr(city, key, value)
        city.save()
        return (jsonify(city.to_dict()), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_post(state_id):
    """ Create new City
    ---
    tags:
        - City
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
    responses:
        201:
            description: City created!
        404:
            description: State not found
        400:
            description: Not a JSON or missing name
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    new = request.get_json()
    new_obj = City(**new)
    setattr(new_obj, "state_id", state_id)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
