''' Module to encapsulate API endpoints related to Weekly Spending. '''

import json
import datetime

from flask import Blueprint, Response, request

from sqlalchemy import func, or_, and_

from utils.weekly_utils import *

from models.database import db
from models.expense import Expense
from models.category import Category
from models.budget import Budget

weekly = Blueprint("weekly", __name__)

# GET weekly summary for the given week
@weekly.route('/summary', methods=['GET'])
def get_weekly_summary():
    
    try:
        # Get week_start param and calculate the week_end date
        query_string_dict = request.args
        week_start = query_string_dict["week_start"]
        week_end = get_week_end(week_start)

        result = db.session.query(Budget.end_date, Budget.amount)\
                        .filter(or_(and_(week_start >= Budget.start_date, week_start <= Budget.end_date),
                                    and_(week_end >= Budget.start_date, week_end <= Budget.end_date))).all()

        if result:

            budgets = list()

            # Write data that is pulled back from the database into the dict
            for r in result:
                budgets.append({
                    "end_date": r[0],
                    "amount": r[1]
                })

            weekly_budget = calculate_weekly_budget(week_start, week_end, budgets)
            
            spent = get_weekly_expenditure(week_start)
            
            if(spent):

                remaining = weekly_budget - spent

                print(spent)
                print(remaining)

                recent = get_recent_weekly(week_start, 5)

                json_response = json.dumps({
                    "spent": spent,
                    "remaining": remaining,
                    "recent": recent
                })

                return json_response

        # Return No Content HTTP response
        return (Response(), 204)

    except:
        # Return Bad Request HTTP response
        return (Response(), 400)