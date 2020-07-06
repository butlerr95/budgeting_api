''' Module to encapsulate API endpoints related to Annual Spending. '''

import json

from flask import Blueprint, Response, request

from sqlalchemy import func

from models.database import db
from models.expense import Expense
from models.category import Category
from models.budget import Budget

annual = Blueprint("annual", __name__)

# GET annual summary for the given year
@annual.route('/<year>', methods=['GET'])
def get_annual_summary(year: str):

    try:
        # Query total expenditure by month for the given year
        result = db.session.query(func.strftime("%m", Expense.date).label("month"), func.sum(Expense.amount).label("total"))\
                        .filter(func.strftime("%Y", Expense.date)==year)\
                        .group_by("month")\
                        .order_by("month").all()

        if result:
            # Initialise all months to have a total of 0, so that months with no expense data are caputured as having a total of 0
            temp_dict = {
                "01": 0.0, "02": 0.0, "03": 0.0, "04": 0.0, "05": 0.0, "06": 0.0,
                "07": 0.0, "08": 0.0, "09": 0.0, "10": 0.0, "11": 0.0, "12": 0.0
            }

            # Write data that is pulled back from the database into the dict
            for result in result:
                temp_dict[result[0]] = result[1]

            json_response = json.dumps(temp_dict)

            return json_response

        else:
            # Return No Content HTTP response
            return (Response(), 204)

    except:
        # Return Bad Request HTTP response
        return (Response(), 400)
