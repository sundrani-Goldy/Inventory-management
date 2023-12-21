# pull the official base image
FROM python:3.11.7

# set work directory
WORKDIR /inventory_management

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update

# RUN apt-get install -y cron && touch /var/log/cron.log

RUN pip install --upgrade pip


COPY ./requirements.txt /inventory_management/
RUN pip install -r requirements.txt
RUN touch /var/container_initialized
# copy project
COPY . /inventory_management/

EXPOSE 8000
CMD ["python", "manage.py", "runserver","127.0.0.1:8000"]