FROM python:3.7-alpine3.11
MAINTAINER Miloslav Pavelka (info@miloslavpavelka.com)

ENV LANG C.UTF-8

# System requirements
RUN set -ex \
	&& apk update \
	&& apk upgrade \
	&& apk add git \
	&& apk add openssl

# Create build environment
RUN set -ex \
	&& apk add --virtual .buildenv python3-dev gcc musl-dev git

# Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN set -ex \
	&& pip install -r /tmp/requirements.txt \
	&& rm /tmp/requirements.txt

# Clean up build environment
RUN set -ex \
	&& apk del .buildenv

# Folder structure
RUN set -ex \
	&& mkdir -p /app \
	&& mkdir -p /conf \
	&& mkdir -p /etc/apache2 \
	&& touch /conf/htpanel.conf

# Application
COPY ./htpanel /app/htpanel
COPY ./templates /app/templates
COPY ./htpanel.py /app/htpanel.py

WORKDIR /app
CMD ["python3", "htpanel.py", "-c", "/conf/htpanel.conf"]
