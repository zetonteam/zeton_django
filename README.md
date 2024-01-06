# zeton_django

Zeton is an application that support behavioral therapy.
Token system for the child.
Allows you to earn points for your activities and exchange them for prizes.

## Application goals

- Developing deficit (desirable) behaviour
- Reduction of undesired behaviour
- Generating and maintaining therapy effects over time

## Dependencies

[Python 3.12](https://www.python.org/downloads/)  
[pip](https://pip.pypa.io/en/stable/installation/)  
[Django 4.2](https://docs.djangoproject.com/en/4.2/)  
[Django Rest Framework](https://www.django-rest-framework.org/)  
[Postgres](https://www.postgresql.org/)

## Docker and docker-compose

1. [Install Docker](https://docs.docker.com/get-docker/)

If you use Linux and need to use `sudo` before `docker compose` command just follow step below:

manage Docker as a non-root
user:  [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)

2. We use Docker Compose V2 which is integrated into Docker Desktop versions. For more information,
   see [Migrate to Compose V2](https://docs.docker.com/compose/migrate/)

3. Commands:

If you want to build and run containers - you can do it in two ways:

Build and run containers:

`docker compose up -d --build`

Or

Build the image:  
`docker compose build`

Fire up cointainers:  
`docker compose up`

Or fire up containers in detached mode:  
`docker compose up -d`

## Database: postgres (Django, docker-compose)

To make migrations and migrate:

```
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

To create superuser:  
`docker compose exec web python manage.py createsuperuser`

## To populate data

To populate data using fixtures:  
`make load_data`

## To rebuild database

If you want rebuild database, you can use command:  
`docker compose down -v`

**WARNING!** This command will delete all data from the database

## Register and login user in the Django app

Go to http://localhost:8000/admin and create a new user.

## Access API

### Auth

To run app with tokens, set `.local.env` `ENVIRONMENT` to `PROD`.

Go to http://localhost:8000/api/users/register/

You may use Postman for that.

As you can see below, you can fill the body form-data with info:

![](https://github.com/zetonteam/zeton_django/blob/develop/images/postman_register_01.png?raw=true)

After that you can hit http://localhost:8000/api/users/students/ with GET method and put into Headers key and value.

Then you have access to private endpoint.

![](https://github.com/zetonteam/zeton_django/blob/develop/images/postman_register_02.png?raw=true)

More private endpoints:

Go to http://localhost:8000/api/users/students/

You may expect this result:

```
[
    {
        "pk": 1,
        "email": "wojtek-zeton@mailinator.com",
        "username": "wojtek",
        "first_name": "Wojtek",
        "last_name": "",
        "total_points": 250
    },
    {
        "pk": 2,
        "email": "kuba-zeton@mailinator.com",
        "username": "kuba",
        "first_name": "Kuba",
        "last_name": "",
        "total_points": 120
    }
]
```

Go to http://localhost:8000/api/users/students/1

Result:

```
{
    "pk": 1,
    "email": "wojtek-zeton@mailinator.com",
    "username": "wojtek",
    "first_name": "Wojtek",
    "last_name": "",
    "total_points": 250
}
```

Go to http://localhost:8000/api/users/prizes/

```
[
    {
        "pk": 1,
        "student": "1",
        "name": "Puszka Coca-cola",
        "value": 10
    },
    {
        "pk": 2,
        "student": "2",
        "name": "1 godzina na basenie",
        "value": 30
    }
]
```

Go to http://localhost:8000/api/users/prizes/1

Result:

```
{
    "pk": 1,
    "student": "1",
    "name": "Puszka Coca-cola",
    "value": 10
}
```

Similarly, tasks:

Go to  
http://localhost:8000/api/users/tasks/  
http://localhost:8000/api/users/tasks/1

## Points endpoints

There are currently several enpoints responsible for managing student points available:

1. `api/users/points/` accesible with a `GET` request and followed by a query string pointing to a student primary
   key.  
   For example: `api/users/points/?studentId=2` should return Point instances assigned to the student with `pk=2`

2. `api/users/points/` accesible with `POST` request, payload in a given format is required:

```
{
    "value": 40,
    "assigner": 1,
    "assignee": 1,
}
```

As a result you should receive a response similar to the following:

```
{
    "pk": 5,
    "value": 40,
    "assigner": 1,
    "assignee": 1,
    "assignment_date": "2021-01-26T21:41:04.952509Z"
}
```

3. `api/users/points/<int:pk>/` accesible with `GET` request, should return single requested Point instance

### Tests

There are also some tests, checking above endpoints, available in the `users/tests/users/test_points.py` module.

To execute the tests simply call `docker compose exec web pytest` (you can add the `-v` flag for a verbose ouput).

## Swagger ui

Our project supports a minimal swagger UI setup for Django Rest Framework,
described [here](https://www.django-rest-framework.org/topics/documenting-your-api/).  
You can access it with [http://localhost:8000/swagger-ui](http://localhost:8000/swagger-ui) endpoint.  
Openapi compliant text documentation: [http://localhost:8000/openapi](http://localhost:8000/openapi)
