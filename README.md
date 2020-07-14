# zeton_django

Zeton is an application that  support behavioral therapy. 
Token system for the child. 
Allows you to earn points for your activities and exchange them for prizes.

## Application goals

- Developing deficit (desirable) behaviour
- Reduction of undesired behaviour
- Generating and maintaining therapy effects over time

## Development setup
Install Python 3.7.2

Create a virtual environment: <br/>
`python3 -m venv venv`

To activate a venv: <br/>
`source venv/bin/activate`

Install dependencies: <br/>
`pip install -r requirements.txt`

## Migrate db:
`python3 manage.py makemigrations` <br>
`python3 manage.py migrate`

## To create an admin account:
`python manage.py createsuperuser`

## To run server:
`python manage.py runserver`

## Access API
ToDo

