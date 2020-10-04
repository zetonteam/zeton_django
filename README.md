# zeton_django

Zeton is an application that  support behavioral therapy. 
Token system for the child. 
Allows you to earn points for your activities and exchange them for prizes.

## Application goals

- Developing deficit (desirable) behaviour
- Reduction of undesired behaviour
- Generating and maintaining therapy effects over time

## Dependencies

[Python 3.8](https://www.python.org/downloads/) <br>
[pip](https://pip.pypa.io/en/stable/installing/) <br>
[Django](https://docs.djangoproject.com/en/3.1/) <br>
[Django Rest Framework](https://www.django-rest-framework.org/) <br>
[Postgres](https://www.postgresql.org/) <br>

## Development setup
Install Python 3.8

Create a virtual environment:
`python3 -m venv venv`

To activate a venv:
`source venv/bin/activate`

Install dependencies:
`pip install -r requirements.txt`

## Migrate db:
`python3 manage.py makemigrations`
`python3 manage.py migrate`

## To create an admin account:
`python manage.py createsuperuser`

## To run server:
`python manage.py runserver`

## Docker and docker-compose

[Install Docker](https://docs.docker.com/get-docker/)
```
docker -v
Docker version 19.03.5, build 633a0ea

docker-compose -v
docker-compose version 1.25.4, build 8d51620a
```

If you want to build and run containers - you can do it in two ways:

Build and run containers: <br>
`docker-compose up -d --build`

Or

Build the image: <br>
`docker-compose build`

Fire up cointainers: <br>
`docker-compose up`

Or fire up containers in detached mode: <br>
`docker-compose up -d`

## Database: postgres (Django, docker-compose)

To make migrations and migrate: <br>
```
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
```

To create superuser: <br>
`docker-compose exec django python manage.py createsuperuser`

## Register and login user in the Django app

Go to http://localhost:8000/admin and create a new user. <br>

## Access API
ToDo

