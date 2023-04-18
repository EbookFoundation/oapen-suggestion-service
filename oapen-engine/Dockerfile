FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv nltk
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential linux-libc-dev python-dev gcc postgresql postgresql-contrib && rm -rf /var/lib/apt/lists/*

# Install python dependencies in /.venv
COPY Pipfile .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --skip-lock --verbose

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
ENV PATH="$PATH:/usr/local/bin"

RUN apt-get update && apt-get install libpq5 -y

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

RUN [ "python", "-c", "import nltk; nltk.download('punkt', download_dir='/home/appuser/nltk_data'); nltk.download('stopwords', download_dir='/home/appuser/nltk_data')" ]

ENV PYTHONPATH="/home/appuser/src"

# Install application into container
COPY . .

USER root

RUN chmod -R +x scripts

USER appuser

# Run the application
ENTRYPOINT ["./scripts/run.sh"]