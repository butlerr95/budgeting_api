# Budgeting API

## About
This is a REST API service for managing Expenses in a database, currently implemented for SQLite.

## Virtual Environment
Create a virtual environment using the command:

    python -m venv venv

## Dependencies
The dependencies can be installed from requirements.txt using the command:

    pip install -r requirements.txt

## Running the Flask server
The Flask server can be run by running the budgeting.py file using the command:

    python budgeting.py

## Pylint
Code quality can be checked in accordance with the PEP8 standard by using the following command, where filename is the name of the python script to be checked:

    pylint filename.py

## Black
Black can be used to format python code automatically using the following command. The -l flag specifies the line length.

    black -l 120 filename.py