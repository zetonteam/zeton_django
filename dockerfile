FROM python:3.12.2
ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/