FROM python:3.9-slim
WORKDIR /code
COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  \
    && pip install poetry \
    && poetry config virtualenvs.create false

RUN chmod +x "runserver.sh"
RUN cd django-package && poetry install --no-dev