import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users")
        call_command("loaddata", "students")
        call_command("loaddata", "caregivers")
        call_command("loaddata", "tasks")
        call_command("loaddata", "prizes")
        call_command("loaddata", "roles")
        call_command("loaddata", "points")
