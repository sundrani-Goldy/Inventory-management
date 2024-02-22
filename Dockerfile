# pull the official base image
FROM python:3.11.7

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update

# RUN apt-get install -y cron && touch /var/log/cron.log

RUN pip install --upgrade pip

# install watchman
RUN apt-get install -y watchman

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
RUN touch /var/container_initialized

# copy project
COPY . /app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
