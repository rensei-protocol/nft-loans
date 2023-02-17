# Use an official Python runtime as a parent image
FROM python:3.9-slim
MAINTAINER Rauan Amangeldiyev, rauan@voyage.finance

# Install poetry
ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    \
    VIRTUAL_ENV=/opt/venv \
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
#    POETRY_VERSION=1.1.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update -yqq && apt-get upgrade -yqq && apt-get install -y --no-install-recommends \
    nano git\
    build-essential netbase \
    libgfortran5 locales zip \
    software-properties-common \
    apt-transport-https ca-certificates gnupg \
    swig potrace \
    wget unzip file curl \
    libpq-dev libspatialindex-dev \
    python3-pip python3-venv && \
    python -m venv $VIRTUAL_ENV &&\
    pip install --no-cache-dir -U pip &&\
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

RUN adduser --disabled-password --gecos '' myuser
