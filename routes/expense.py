''' Module to encapsulate API endpoints related to Expense. '''

import json

from flask import Blueprint, Response, request

from models.database import db
from models.expense import Expense
from models.category import Category

expense = Blueprint("expense", __name__)

# GET all expenses
@expense.route('/', methods=['GET'])
def get_expenses():
    
    try:
        expenses = Expense.query\
            .join(Category, Expense.category_id==Category.id)\
            .with_entities(Expense.id, Expense.date, Category.name, Expense.description, Expense.amount)\
            .all()

        if expenses is None:
                return (Response(), 404)

        response = list()
        for expense in expenses:
            temp_dict = dict()
            temp_dict["id"] = expense[0]
            temp_dict["date"] = expense[1]
            temp_dict["category"] = expense[2]
            temp_dict["description"] = expense[3]
            temp_dict["amount"] = expense[4]
            response.append(temp_dict)

        json_response = json.dumps(response)

        return json_response
        
    except:
        db.session.rollback()
        return (Response(), 400)


# GET expense by ID
@expense.route('/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
        
    try:
        expense = Expense.query\
            .filter_by(id=expense_id)\
            .join(Category, Expense.category_id==Category.id)\
            .with_entities(Expense.id, Expense.date, Category.name, Expense.description, Expense.amount)\
            .first()

        if expense is None:
            return (Response(), 404)

        response = dict()
        response["id"] = expense[0]
        response["date"] = expense[1]
        response["category"] = expense[2]
        response["description"] = expense[3]
        response["amount"] = expense[4]

        json_response = json.dumps(response)

        return json_response
    
    except:
        db.session.rollback()
        return (Response(), 400)

# POST expense
@expense.route('/', methods=['POST'])
def create_expense():

    try:
        data = request.json
        expense = Expense(data["date"], data["category_id"], data["budget_id"], data["description"], data["amount"])
        db.session.add(expense)
        db.session.commit()
        return (Response(), 200)

    except:
        db.session.rollback()
        return (Response(), 400)

    # IMPLEMENT ERROR HANDLING FOR WHEN DATA OBJECT DOES NOT CONTAIN EXPECTED KEYS

# PUT expense
@expense.route('/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    
    try:
        expense = Expense.query.filter_by(id=expense_id).first()
        if expense is None:
            return (Response(), 404)
        else:
            data = request.json
            expense.date = data["date"]
            expense.category_id = data["category_id"]
            expense.budget_id = data["budget_id"]
            expense.description = data["description"]
            expense.amount = data["amount"]
            db.session.commit()
            return (Response(), 200)

    except:
        db.session.rollback()
        return (Response(), 400)

# DELETE expense
@expense.route('/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):

    try:
        expense = Expense.query.filter_by(id=expense_id).first()
        if expense is None:
            return (Response(), 404)
        else:
            Expense.query.filter_by(id=expense_id).delete()
            db.session.commit()
            return (Response(), 200)

    except exc.IntegrityError as e:
        db.session.rollback()
        return (Response(), 409)

    except:
        db.session.rollback()
        return (Response(), 400)
