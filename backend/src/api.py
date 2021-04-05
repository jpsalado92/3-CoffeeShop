import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()  # THIS WILL DROP ALL RECORDS AND START THE DB FROM SCRATCH


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except:
        abort(404)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except:
        abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    body = request.get_json()
    try:
        if 'title' and 'recipe' not in body:
            abort(422)

        title = body['title']
        recipe = json.dumps(body['recipe'])

        drink = Drink(title=title, recipe=recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except:
        abort(404)


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink_id(payload, id):
    try:
        body = request.get_json()
        drink = Drink.query.get(id)
        title = body['title']

        if 'recipe' in body.keys():
            recipe = json.dumps(body['recipe'])
        else:
            recipe = drink.recipe

        drink.title = title
        drink.recipe = recipe
        drink.update()
        return jsonify({
            "success": True,
            "drinks": [drink.long(),]
        }), 200
    except:
        abort(404)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        Drink.query.get(id).delete()
        return jsonify({
            "success": True,
            "delete": id
        }), 200
    except:
        abort(404)


# Error Handling
@app.errorhandler(401)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422
