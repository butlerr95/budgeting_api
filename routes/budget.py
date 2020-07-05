''' Module to encapsulate API endpoints related to Budget. '''

import json

from flask import Blueprint, Response, request

from models.database import db
from models.budget import Budget

budget = Blueprint("budget", __name__)

# GET all budgets
@budget.route('/', methods=['GET'])
def get_budgets():

    try:
        budgets = Budget.query\
            .with_entities(Budget.id, Budget.start_date, Budget.end_date, Budget.amount)\
            .all()

        if budgets is None:
            return (Response(), 404)

        response = list()
        for budget in budgets:
            temp_dict = dict()
            temp_dict["id"] = budget[0]
            temp_dict["start_date"] = budget[1]
            temp_dict["end_date"] = budget[2]
            temp_dict["amount"] = budget[3]
            response.append(temp_dict)

        json_response = json.dumps(response)

        return json_response

    except:
        db.session.rollback()
        return (Response(), 400)


# GET budget by ID
@budget.route('/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    
    try:
        budget = Budget.query\
            .filter_by(id=budget_id)\
            .with_entities(Budget.id, Budget.start_date, Budget.end_date, Budget.amount)\
            .first()

        if category is None:
            return (Response(), 404)

        response = dict()
        response["id"] = budget[0]
        response["start_date"] = budget[1]
        response["end_date"] = budget[2]
        response["amount"] = budget[3]

        json_response = json.dumps(response)

        return json_response

    except:
        db.session.rollback()
        return (Response(), 400)


# POST budget
@budget.route('/', methods=['POST'])
def create_budget():

    try:
        data = request.json
        budget = Budget(data["start_date"], data["end_date"], data["amount"])
        db.session.add(budget)
        db.session.commit()
        return (Response(), 200)

    except:
        db.session.rollback()
        return (Response(), 400)

    # IMPLEMENT ERROR HANDLING FOR WHEN DATA OBJECT DOES NOT CONTAIN EXPECTED KEYS


# PUT budget
@budget.route('/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):

    try:
        data = request.json
        budget = Budget.query.filter_by(id=budget_id).first()
        if budget is None:
            return (Response(), 404)
        else:
            budget.start_date = data["start_date"]
            budget.end_date = data["end_date"]
            budget.amount = data["amount"]
            db.session.commit()
            return (Response(), 200)

    except:
        db.session.rollback()
        return (Response(), 400)


# DELETE budget
@budget.route('/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    
    try:
        budget = Budget.query.filter_by(id=budget_id).first()
        if budget is None:
            return (Response(), 404)
        else:
            Budget.query.filter_by(id=budget_id).delete()
            db.session.commit()
            return (Response(), 200)

    except exc.IntegrityError as e:
        db.session.rollback()
        return (Response(), 409)

    except:
        db.session.rollback()
        return (Response(), 400)
