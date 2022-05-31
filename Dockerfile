FROM python:3.8-slim
WORKDIR /code
COPY ./myappcalendar/ .
COPY django-package django-package

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  \
    && pip install poetry \
    && poetry config virtualenvs.create false

RUN cd django-package && poetry install --no-dev