#!/usr/bin/python3
""" Methods that handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/reviews/<review_id>')
def reviews(review_id=None):
    """ Show review
    ---
    tags:
        - Review
    parameters:
      - name: review_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show review
      404:
        description: Resource not found
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews')
def review_place(place_id=None):
    """ Show reviews by place
    ---
    tags:
        - Review
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show reviews
      404:
        description: Resource not found
    """
    reviews = []
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['DELETE', 'PUT'])
def review_delete(review_id=None):
    """ Update review
    ---
    tags:
        - Review
    parameters:
      - name: review_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Review updated
      404:
        description: Resource not found
      400:
        description: Not a JSON
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        to_update = request.get_json()
        for key, value in to_update.items():
            if (key is not "id" and key is not "created_at" and
                    key is not "updated_at" and key is not "user_id" and
                    key is not "place_id"):
                setattr(review, key, value)
        review.save()
        return (jsonify(review.to_dict()), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_post(place_id):
    """ Create a reate in place
    ---
    tags:
        - Review
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
    responses:
      201:
        description: Review created!
      404:
        description: Resource not found
      400:
        description: Not a JSON or/and missing text or/and missing user_id
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'text' not in request.json:
        abort(400, "Missing text")
    new = request.get_json()
    user_id = new.get("user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_obj = Review(**new)
    setattr(new_obj, "place_id", place_id)
    storage.new(new_obj)
    storage.save()
    return (jsonify(new_obj.to_dict()), 201)
