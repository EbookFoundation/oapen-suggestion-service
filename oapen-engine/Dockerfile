FROM python:3.10-slim as base

RUN apt update
RUN apt install build-essential -y --no-install-recommends

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --skip-lock

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv

RUN mkdir /proj
WORKDIR /proj

ENV PATH="/usr/local/bin:/.venv/bin:$PATH"

# Install application into container
COPY . .

ENTRYPOINT PIPENV_VENV_IN_PROJECT=1 /usr/local/bin/pipenv python tasks/generate_suggestions.py
