FROM python:3.9

RUN apt-get update && \
    apt-get -y install --no-install-recommends curl make && \
    rm -rf /var/lib/apt/lists/*

ARG APP_DIR=/app

ENV PATH=/root/.poetry/bin:${PATH} \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.1.4 \
    POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR $APP_DIR

COPY entrypoint.sh Makefile Pipfile Pipfile.lock README.md .env ./
RUN chmod +x entrypoint.sh
RUN make install-packages

COPY server/ ./server
COPY tests/ ./tests

ARG BUILD_RELEASE
ENV BUILD_RELEASE=${BUILD_RELEASE}

CMD ["sh","entrypoint.sh"]

