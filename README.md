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

- After modifying endpoints - make sure `Endpoints` table below is up to date.

- Make sure new endpoint contains all necessary tests.

## Endpoints

| URL                                            | Operation | Implementation | Tests | Description                              |
|------------------------------------------------|-----------|----------------|-------|------------------------------------------|
| token-auth                                     | POST      | ✅              | ✅     | Authentication token for a user.         |
| current-user                                   | GET       | ✅              | ✅     | Current user by their token.             |
| students                                       | GET       | ✅              | ✅     | All students for logged-in caregiver.    |
| students                                       | POST      | ❌              | ❌     | Add new student for a caregiver.         |
| students/<int:student_id>                      | GET       | ✅              | ✅     | Info about student with given ID.        |
| students/<int:student_id>                      | PATCH     | ✅              | ✅     | Update info about student with given ID. |
| students/<int:student_id>/points               | GET       | ✅              | ✅     | Points history of a student.             |
| students/<int:student_id>/points               | POST      | ✅              | ❌     | Add points to a student.                 |
| students/<int:student_id>/prize/<int:prize_id> | GET       | ✅              | ✅     | Info about prize with given ID.          |
| students/<int:student_id>/prize/<int:prize_id> | PATCH     | ✅              | ✅     | Edit a prize.                            |
| students/<int:student_id>/prize/<int:prize_id> | DELETE    | ✅              | ❌     | Delete a prize.                          |
| students/<int:student_id>/prizes               | GET       | ✅              | ✅     | Prizes assigned to a student.            |
| students/<int:student_id>/prizes               | POST      | ✅              | ✅     | Add new prize to a student.              |
| students/<int:student_id>/task/<int:task_id>   | GET       | ✅              | ❌     | Task assigned to a student.              |
| students/<int:student_id>/task/<int:task_id>   | PATCH     | ✅              | ❌     | Edit a task.                             |
| students/<int:student_id>/task/<int:task_id>   | DELETE    | ✅              | ❌     | Delete a task.                           |
| students/<int:student_id>/tasks                | GET       | ✅              | ❌     | Tasks assigned to a student.             |
| students/<int:student_id>/tasks                | POST      | ✅              | ❌     | Assign a task to a student.              |
| caregivers                                     | POST      | ❌              | ❌     | Add a new caregiver.                     |
| roles                                          | POST      | ❌              | ❌     | Add a new role.                          |
