# syntax=docker/dockerfile:1
FROM python:3.10 as base

ENV IN_DOCKER 1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY etc/ etc/
COPY requirements.txt .
COPY Makefile .

COPY src src

RUN groupadd -g 1000 uwsgi && \
    useradd -r -m -u 1000 -g uwsgi uwsgi && \
    chown -R uwsgi:uwsgi /app

EXPOSE 8000

#################### Production image. ####################
FROM base as prod

RUN make venv/.venv_prod
RUN make collectstatic

CMD ["make", "run/webserver"]

#################### Test image. ####################
FROM base as test

COPY requirements ./requirements

# for black and isort config
COPY pyproject.toml .
COPY setup.cfg .

RUN make venv/.venv_test

CMD ["make", "test"]

#################### Dev image. ####################
FROM test as dev

RUN make venv

CMD ["/bin/bash"]