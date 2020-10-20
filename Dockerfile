FROM python:3-alpine as base

ARG BUILD_DATE
ARG VCS_REF

LABEL maintainer="Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>" \
    org.opencontainers.image.title="SVM Image" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.version="0.1.1" \
    org.opencontainers.image.url="git.ufz.de:4567/rdm-software/svm/backend:$BUILD_DATE" \
    org.opencontainers.image.revision=$VCS_REF \
    org.opencontainers.image.created=$BUILD_DATE

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk --no-cache add libpq

FROM base as builder

RUN mkdir /install
WORKDIR /install

# add requirements
COPY app/requirements.txt /tmp/requirements.txt

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --upgrade pip \
    && pip install --prefix /install --no-cache-dir -r /tmp/requirements.txt \
    && apk del --no-cache .build-deps

FROM base

COPY --from=builder /install /usr/local

# add app
COPY app /usr/src/app

#run server
CMD ["sh", "-c","pip install --no-cache-dir -r requirements.txt && gunicorn --access-logfile - -b 0.0.0.0:5000 manage:app"]
EXPOSE 5000

# docker run --rm -p 127.0.0.1:5000:5000 -e DATABASE_URL="postgres://postgres:postgres@db:5432/db_dev" -e APP_SETTINGS="project.config.DevelopmentConfig" git.ufz.de:4567/rdm-software/svm/backend:latest
