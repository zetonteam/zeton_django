FROM python:3.12.6

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/code

RUN mkdir /code
WORKDIR /code
COPY poetry.lock /code/
COPY pyproject.toml /code/

RUN pip install -U pip wheel "poetry==${POETRY_VERSION}"

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-ansi

COPY . /code/
