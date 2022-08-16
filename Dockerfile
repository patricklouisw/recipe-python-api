FROM python:3.9-alpine3.13
LABEL maintainer="LOUISPAT"

# This is so we can see the logs from the container in our terminal
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Set a buil argument Dev to false by default and DEV can be manually set in docker-compose.yaml (if you want to run DEV environbment)
ARG DEV=false
# 1.venv: create a python virtual environment (to make sure that any dependencies in the base image wouldn't conflict with our project)
# 2. upgrade pip
#3. install whatever in requirements
#4. remove directory
#5. Add new user django-user (with no password and no creation of home directory) -> BEST practice as this user will have limited privileges in case the container is compromised and make the container lean.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "TRUE" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user


ENV PATH="/py/bin:$PATH"

USER django-user