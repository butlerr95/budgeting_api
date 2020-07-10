''' Module to create the Flask app. '''

from flask import Flask
from sqlalchemy import event

from models.database import db
from routes.expense import expense as expense_routes
from routes.category import category as category_routes
from routes.budget import budget as budget_routes
from routes.annual import annual as annual_routes
from routes.weekly import weekly as weekly_routes
from routes.monthly import monthly as monthly_routes

def create_app():
	''' Creates and returns the Flask app by loading config, 
    	registering blueprints and initialising the DB. '''

	app = Flask(__name__)
	app.config.from_object('config.Config')

	app.register_blueprint(expense_routes, url_prefix="/expense")
	app.register_blueprint(category_routes, url_prefix="/category")
	app.register_blueprint(budget_routes, url_prefix="/budget")
	app.register_blueprint(annual_routes, url_prefix="/annual")
	app.register_blueprint(weekly_routes, url_prefix="/weekly")
	app.register_blueprint(monthly_routes, url_prefix="/monthly")

	db.init_app(app)

	# Ensure FOREIGN KEY constraint for sqlite3
	if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
		def _fk_pragma_on_connect(db, conn_record):  # noqa
			db.execute('pragma foreign_keys=ON')

		with app.app_context():
			event.listen(db.engine, 'connect', _fk_pragma_on_connect)

			# Create database and tables if they don't exist
			db.create_all()

	return app
