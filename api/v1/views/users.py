#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users')
@app_views.route('/users/<user_id>')
def users(user_id=None):
    """ Show User
    ---
    tags:
        - User
    parameters:
      - name: user_id
        in: path
        type: string
    responses:
      200:
        description: List of users
      404:
        description: Resource not found
    """
    users = []
    if user_id:
        user = storage.get("User", user_id)
        if user is None:
            abort(404, description="Resource not found")
        else:
            return jsonify(user.to_dict())
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('users/<user_id>', methods=['DELETE', 'PUT'])
def user_delete_update(user_id=None):
    """ Update user
    ---
    tags:
        - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: User updated
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        to_update = request.get_json()
        for key, value in to_update.items():
            if (key is not "id" and key is not "created_at" and
                    key is not "updated_at" and key is not "email"):
                setattr(user, key, value)
        user.save()
        return (jsonify(user.to_dict()), 200)


@app_views.route('/users', methods=['POST'])
def user_post():
    """ Create user
    ---
    tags:
        - User
    responses:
      201:
        description: User created
      400:
        description: Missing password or/and email
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    new = request.get_json()
    new_obj = User(**new)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
