# zeton_django

Django-based backend for Żeton application.

## Dependencies

- [Python 3.12](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Django 4.2](https://docs.djangoproject.com/en/4.2/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Postgres](https://www.postgresql.org/)

## Development environment setup

Following instructions assume Ubuntu 24.04-based configuration.

### Install `pipx`

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

### Install Poetry

```bash
pipx install poetry
```

### Install Poetry dependencies

Following command installs dependencies based on `pyproject.toml`:

```bash
poetry install
```

#### Other helpful poetry commands

- Add a new dependency: `poetry add <DEPENDENCY_NAME>`.

Both `pyproject.toml` and `poetry.lock` will be modified.

- Get the altest version of all dependencies: `poetry update`.

`poetry.lock` will be updated.

- Execute a command inside the project's virtual environment: `poetry run command`.

- Spawn a shell within the project's virtual environment: `poetry shell`.

### Install `pre-commit`

```bash
pipx install pre-commit
pre-commit install
```

### Docker set-up

Install Docker using following instructions:

- [Instructions for Windows/Mac](https://docs.docker.com/desktop/)
- [Instructions for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)

Build images:

```bash
docker compose build
```

Run containers:

```bash
docker compose up
```

`-d` can be added to run containers in detached mode.

### Database set-up

Make migrations:

```bash
docker compose exec web python manage.py makemigrations
```

Run migration:

```bash
docker compose exec web python manage.py migrate
```

Populate database using fixtures:

```bash
docker compose exec web bash -c "python manage.py loaddata fixtures/*.json"
```

#### Other helpful database commands

Create new super-user:

```bash
docker compose exec web python manage.py createsuperuser
```

Tear down database:

```bash
docker compose down -v
```

**WARNING!** This command will delete all data from the database

## Contributing

- Make sure all pre-commit hooks are passing.

```bash
pre-commit run -a
```

## Register and login user in the Django app

Go to http://localhost:8000/admin and create a new user.

## Access API

### Getting authentication token

To get authentication token use:

```bash
./scripts/get_token.py --username <USERNAME> --password <PASSWORD> | jq -r .access
```

Default data fixture is using `opiekun1` both for username and password.

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

2. `api/users/points/` accessible with `POST` request, payload in a given format is required:

```
{
    "value": 40,
    "assigner": 1,
    "student": 1,
}
```

As a result you should receive a response similar to the following:

```
{
    "pk": 5,
    "value": 40,
    "assigner": 1,
    "student": 1,
    "assignment_date": "2021-01-26T21:41:04.952509Z"
}
```


### Tests

There are also some tests, checking above endpoints, available in the `users/tests/users/test_points.py` module.

To execute the tests simply call `docker compose exec web pytest` (you can add the `-v` flag for a verbose ouput).

## Planned endpoints

### GET /api/students  / DONE

List all students for logged in caregiver

### POST /api/students (future)

Add new student for a caregiver

### GET /api/students/<id:int> / DONE

Retrieve information about student with given ID:
- ...
- total_points

### PATCH /api/students/<id:int> / DONE

Update student

### GET /api/students/<id:int>/points / DONE

List history of points received by student

### POST /api/students/<id:int>/points (no longer needed)

~~Add new points to student~~
Points should be automatically added when completing a task (another endpoint)
 (session012)
### GET /api/students/<id:int>/tasks | DONE

List of tasks assigned to student

### POST /api/students/<id:int>/tasks | DONE

Add new task for student

### PATCH /api/students/<id:int>/tasks/<task_id:int>

Edit existing task + soft delete

### GET /api/students/<id:int>/prizes / DONE

List of prizes assigned to student

### POST /api/students/<id:int>/prizes / DONE

Add new prize for student

### PATCH /api/students/<id:int>/prizes/<prize_id:int>

Edit existing prize + soft delete

### POST /api/students/<id:int>/tasks/<task_id:int>/reward

Add points to student for a completed task

### POST /api/students/<id:int>/prizes/<prize_id:int>/claim

Exchange points for prize

### POST /api/caregivers (future)

Add new caregiver

### POST /api/roles (future)

Add new role (association between student and caregiver)

## Swagger ui

Our project supports a minimal swagger UI setup for Django Rest Framework,
described [here](https://www.django-rest-framework.org/topics/documenting-your-api/).
You can access it with [http://localhost:8000/swagger-ui](http://localhost:8000/swagger-ui) endpoint.
Openapi compliant text documentation: [http://localhost:8000/openapi](http://localhost:8000/openapi)
