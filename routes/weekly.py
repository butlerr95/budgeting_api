''' Module to encapsulate API endpoints related to Weekly Spending. '''

import json
import datetime

from flask import Blueprint, Response, request

from sqlalchemy import or_, and_

from utils.weekly_utils import *

from models.database import db
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

        # Get all budgets that lie within week_start and week_end
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

            # Calculate the weekly budget based on the budget(s) extracted from the db
            weekly_budget = calculate_weekly_budget(week_start, week_end, budgets)
            
            # Get the total spent for the week
            spent = get_weekly_expenditure(week_start)
            
            if(spent):
                # Calculate remaining based on the weekly budget and amount spent
                remaining = weekly_budget - spent

                # Get the 5 most recent expenses in the current week
                recent = get_recent_weekly(week_start, 5)

                # Serialise to json
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