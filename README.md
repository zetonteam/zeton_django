# zeton_django

Zeton is an application that  support behavioral therapy. 
Token system for the child. 
Allows you to earn points for your activities and exchange them for prizes.

## Application goals

- Developing deficit (desirable) behaviour
- Reduction of undesired behaviour
- Generating and maintaining therapy effects over time

## Dependencies

[Python 3.8](https://www.python.org/downloads/)  
[pip](https://pip.pypa.io/en/stable/installing/)  
[Django](https://docs.djangoproject.com/en/3.1/)  
[Django Rest Framework](https://www.django-rest-framework.org/)  
[Postgres](https://www.postgresql.org/)  

## Docker and docker-compose

[Install Docker](https://docs.docker.com/get-docker/)

If you want to build and run containers - you can do it in two ways:

Build and run containers:

`docker-compose up -d --build`

Or

Build the image:  
`docker-compose build`

Fire up cointainers:  
`docker-compose up`

Or fire up containers in detached mode:  
`docker-compose up -d`

## Database: postgres (Django, docker-compose)

To make migrations and migrate:  
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

To create superuser:  
`docker-compose exec web python manage.py createsuperuser`

## Register and login user in the Django app

Go to http://localhost:8000/admin and create a new user.  

## Access API
ToDo

