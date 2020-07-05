''' Module to define the Budget object, which is a SQLAlchemy model '''

from .database import db

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, start_date, category_id, description, amount):
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
