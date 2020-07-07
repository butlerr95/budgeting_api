''' Module to hold functionality related to weekly expenses '''

import math
import datetime

from sqlalchemy import func, and_

from models.database import db
from models.expense import Expense
from models.category import Category

def get_recent_weekly(week_start: str, number_expenses: int):

    week_end = get_week_end(week_start)

    result = Expense.query\
            .filter(and_(Expense.date >= week_start, Expense.date <= week_end))\
            .join(Category, Expense.category_id==Category.id)\
            .with_entities(Expense.id, Expense.date, Category.name, Expense.description, Expense.amount)\
            .order_by(Expense.date.desc())\
            .limit(number_expenses)\
            .all()

    if result:

        expenses = list()

        # Write data that is pulled back from the database into the dict
        for r in result:
            expenses.append({
                "id": r[0],
                "date": r[1],
                "category": r[2],
                "description": r[3],
                "amount": r[4]
            })

        return expenses

def get_weekly_expenditure(week_start: str):

    week_end = get_week_end(week_start)

    result = db.session.query(func.sum(Expense.amount).label("total"))\
                        .filter(and_(Expense.date >= week_start, Expense.date <= week_end)).first()

    if result:
        return result[0]

def get_week_end(week_start: str) -> str:
    ''' Get the week_end date for a given week_start date '''

    week_end_date = datetime.datetime.strptime(week_start, r"%Y-%m-%d") + datetime.timedelta(days=6)
    week_end = week_end_date.strftime(r"%Y-%m-%d")

    return week_end

# todo: test this
def calculate_weekly_budget(week_start: str, week_end: str, budgets: list) -> float:
    ''' Calculate the weekly budget based on the budgets that the current week lies within '''

    weekly_budget = 0

    # In the case that there is just one budget in the week range, convert the amount to weekly, round down and return
    if len(budgets) <= 1:
        weekly_budget = (budgets[0]["amount"] * 12) / 52
        return math.floor(weekly_budget / 0.01) * 0.01

    week_start_date = datetime.datetime.strptime(week_start, r"%Y-%m-%d")
    week_end_date = datetime.datetime.strptime(week_end, r"%Y-%m-%d")

    # Set the current date as the start of the week
    current_date = week_start_date

    for budget in budgets:
        # Get the budget end date
        budget_end = datetime.datetime.strptime(budget["end_date"], r"%Y-%m-%d")

        # If budget end is past end of week, then set budget end to week end
        if budget_end > week_end_date:
            budget_end = week_end_date

        # Calculate number of days between the current day and the budget end date
        number_of_days = abs((budget_end - current_date).days) + 1
        # Calculate the budget per day from the budget[amount] (which is monthly)
        daily_budget = ((budget["amount"] * 12) / 52) / 7
        # Add the daily budget, multiplied by the number of days in this budget, to the weekly_budget, rounding down to the nearest 0.01
        weekly_budget += math.floor((daily_budget * number_of_days) / 0.01) * 0.01
        # Set current date to be the day after the end of this budget
        current_date = budget_end + datetime.timedelta(days=1)

    return weekly_budget
