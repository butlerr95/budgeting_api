''' Module to encapsulate API endpoints related to Weekly Spending. '''

import json
import datetime
import math

from flask import Blueprint, Response, request

from sqlalchemy import func, or_, and_

from models.database import db
from models.expense import Expense
from models.category import Category
from models.budget import Budget

monthly = Blueprint("monthly", __name__)

# GET monthly summary for the given month
@monthly.route('/summary', methods=['GET'])
def get_monthly_summary():
    
    # Get week_start param and calculate the week_end date
    query_string_dict = request.args
    month_start = query_string_dict["month_start"]

    # Get all dates in month
    current_date = datetime.datetime.strptime(month_start, r"%Y-%m-%d")
    month_end_date = datetime.datetime(current_date.year + (current_date.month == 12), 
            (current_date.month + 1 if current_date.month < 12 else 1), 1) - datetime.timedelta(days=1)
    
    month_end = month_end_date.strftime(r"%Y-%m-%d")

    dates = dict()

    result = db.session.query(Expense.date, func.sum(Expense.amount).label("total"))\
                    .filter(Expense.date >= month_start, Expense.date <= month_end)\
                    .group_by(Expense.date)\
                    .all()

    result_dict = dict()

    for r in result:
        result_dict[r[0]] = r[1]

    cumulative_total = 0

    # Loop through all dates in month and update cumulative total from results
    while current_date <= month_end_date:
        date = current_date.strftime(r"%Y-%m-%d")

        if date in result_dict.keys():
            cumulative_total += result_dict[date]
            
        dates[current_date.strftime(r"%Y-%m-%d")] = math.floor(cumulative_total / 0.01) * 0.01

        current_date = current_date + datetime.timedelta(days=1)

    json_response = json.dumps(dates)

    return json_response