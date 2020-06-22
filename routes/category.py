''' Module to encapsulate API endpoints related to Category. '''

import json

from flask import Blueprint, Response, request

from models.database import db
from models.category import Category

category = Blueprint("category", __name__)

# GET all categories
@category.route('/', methods=['GET'])
def get_categories():

    try:
        categories = Category.query\
            .with_entities(Category.id, Category.name)\
            .all()

        if categories is None:
            return (Response(), 404)

        response = list()
        for category in categories:
            temp_dict = dict()
            temp_dict["id"] = category[0]
            temp_dict["name"] = category[1]
            response.append(temp_dict)

        json_response = json.dumps(response)

        return json_response

    except:
        db.session.rollback()
        return (Response(), 400)


# GET category by ID
@category.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    
    try:
        category = Category.query\
            .filter_by(id=category_id)\
            .with_entities(Category.id, Category.name)\
            .first()

        if category is None:
            return (Response(), 404)

        response = dict()
        response["id"] = category[0]
        response["name"] = category[1]

        json_response = json.dumps(response)

        return json_response

    except:
        db.session.rollback()
        return (Response(), 400)


# POST category
@category.route('/', methods=['POST'])
def create_category():

    try:
        data = request.json
        category = Category(data["name"])
        db.session.add(category)
        db.session.commit()
        return (Response(), 200)

    except:
        db.session.rollback()
        return (Response(), 400)

    # IMPLEMENT ERROR HANDLING FOR WHEN DATA OBJECT DOES NOT CONTAIN EXPECTED KEYS


# PUT category
@category.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):

    try:
        data = request.json
        category = Category.query.filter_by(id=category_id).first()
        if category is None:
            return (Response(), 404)
        else:
            category.name = data["name"]
            db.session.commit()
            return (Response(), 200)

    except:
        db.session.rollback()
        return (Response(), 400)


# DELETE category
@category.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    
    try:
        category = Category.query.filter_by(id=category_id).first()
        if category is None:
            return (Response(), 404)
        else:
            Category.query.filter_by(id=category_id).delete()
            db.session.commit()
            return (Response(), 200)

    except exc.IntegrityError as e:
        db.session.rollback()
        return (Response(), 409)

    except:
        db.session.rollback()
        return (Response(), 400)
