#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/<id>')
@app_views.route('/states')
def state(id=None):
    """Show states
    ---
    tags:
        - States
    parameters:
      - name: id
        in: path
        type: string
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
     """
    states = []
    if id:
        state = storage.get("State", id)
        if state is None:
            abort(404, description="Resource not found")
        else:
            return jsonify(state.to_dict())

    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<id>', methods=['DELETE', 'PUT'])
def state_delete_put(id=None):
    """ Updating a State
    ---
    tags:
        - States
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: State updated
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    state = storage.get("State", id)
    if state is None:
        abort(404)
    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        to_update = request.get_json()
        for key, value in to_update.items():
            if (key is not "id" and key is not "created_at" and
               key is not "updated_at"):
                setattr(state, key, value)
        state.save()
        return (jsonify(state.to_dict()), 200)


@app_views.route('/states', methods=['POST'])
def state_post():
    """ Creating new State
    ---
    tags:
        - States
    responses:
      201:
        description: State updated
        examples:
          state: {"name": "Santander"}
      404:
        description: Not a Json or missing name
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    new = request.get_json()
    new_obj = State(**new)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
