''' Module to define configuration class. '''

from os import path

# Get current directory
base_directory = path.abspath(path.dirname(__file__))

class Config():

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(base_directory, 'budgeting.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
