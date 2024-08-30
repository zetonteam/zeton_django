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

- Get the latest version of all dependencies: `poetry update`.

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

### Authentication

To get authentication token use:

```bash
./scripts/get_token.py --username <USERNAME> --password <PASSWORD> | jq -r .access
```

Default data fixture is using `opiekun1` both for username and password.

### Tests

To execute tests use:

```bash
docker compose exec web pytest
```

`-v` can be added for more verbose output.

### Swagger UI and OpenAPI

Swagger UI can be accessed with:

```plain
http://localhost:8000/swagger-ui
```

OpenAPI compliant text documentation can be accessed with:

```plain
http://localhost:8000/openapi
```

## Contributing

- Make sure all pre-commit hooks are passing.

```bash
pre-commit run -a
```

## Endpoints

| URL                                           | Operation | Implementation | Tests | Description                                |
| --------------------------------------------- | --------- | -------------- | ----- | ------------------------------------------ |
| token-auth                                    | GET       | ✅             | ✅    | Authentication token for a user.           |
| current-user                                  | GET       | ✅             | ✅    | Current user by their token.               |
| students                                      | GET       | ✅             | ❌    | All students for logged-in caregiver.      |
| students                                      | POST      | ❌             | ❌    | Add new student for a caregiver.           |
| students/<int:id>                             | GET       | ✅             | ❌    | Info about student with given ID.          |
| students/<int:id>                             | PATCH     | ✅             | ❌    | Update info about student with given ID.   |
| students/<int:id>/points                      | GET       | ✅             | ❌    | Points history of a student.               |
| students/<int:id>/tasks                       | GET       | ✅             | ❌    | Tasks assigned to a student.               |
| students/<int:id>/tasks                       | POST      | ✅             | ❌    | Assign a task to a student.                |
| students/<int:id>/tasks/<int:task_id>         | PATCH     | ❌             | ❌    | Edit a task. Soft delete a task.           |
| students/<int:id>/tasks/<int:task_id>/reward  | POST      | ❌             | ❌    | Reward a student with points.              |
| students/<int:id>/prizes                      | GET       | ✅             | ❌    | Prizes assigned to a student.              |
| students/<int:id>/prizes                      | POST      | ✅             | ❌    | Add new prize to a student.                |
| students/<int:id>/prizes/<int:prize_id>/      | PATCH     | ❌             | ❌    | Edit a prize. Soft delete a prize.         |
| students/<int:id>/prizes/<int:prize_id>/claim | POST      | ❌             | ❌    | Exchange points for a prize.               |
| caregivers                                    | POST      | ❌             | ❌    | Add a new caregiver.                       |
| roles                                         | POST      | ❌             | ❌    | Add a new role.                            |
