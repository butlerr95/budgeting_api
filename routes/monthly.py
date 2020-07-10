''' Module to encapsulate API endpoints related to Weekly Spending. '''

import json
import datetime

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
    # TODO: Calculate month end from month start!
    month_end = query_string_dict["month_end"]

    # Get all dates in month
    current_date = datetime.datetime.strptime(month_start, r"%Y-%m-%d")
    month_end_date = datetime.datetime.strptime(month_end, r"%Y-%m-%d")

    dates = dict()

    while current_date <= month_end_date:
        dates[current_date.strftime(r"%Y-%m-%d")] = 0
        current_date = current_date + datetime.timedelta(days=1)

    result = db.session.query(Expense.date, func.sum(Expense.amount).label("total"))\
                    .filter(Expense.date >= month_start, Expense.date <= month_end)\
                    .group_by(Expense.date)\
                    .all()

    cumulative_total = 0

    # TODO: Cumulative total of all days, not just the ones that have expenditure data!

    for r in result:
        cumulative_total += r[1]
        dates[r[0]] = cumulative_total

    json_response = json.dumps(dates)

    return json_response