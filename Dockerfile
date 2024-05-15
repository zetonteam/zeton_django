FROM python:3.12.1

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code
COPY poetry.lock /code/
COPY pyproject.toml /code/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /code/
