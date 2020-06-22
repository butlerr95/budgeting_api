''' Module to create the Flask app. '''

from flask import Flask
from sqlalchemy import event

from models.database import db
from routes.expense import expense as expense_routes
from routes.category import category as category_routes

def create_app():
''' Creates and returns the Flask app by loading config, 
    registering blueprints and initialising the DB. '''

    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.register_blueprint(expense_routes, url_prefix="/expense")
    app.register_blueprint(category_routes, url_prefix="/category")

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
