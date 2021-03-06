''' Module to define the Expense object, which is a SQLAlchemy model '''

from .database import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, date, category_id, budget_id, description, amount):
        self.date = date
        self.category_id = category_id
        self.budget_id = budget_id
        self.description = description
        self.amount = amount
