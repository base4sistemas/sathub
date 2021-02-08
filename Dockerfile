FROM python:3.8-alpine

WORKDIR /home/sathub

COPY ./requirements/base.txt requirements.txt

COPY ./dll/sat.ini /var/tanca_jetway/sat.ini

RUN apk --no-cache add \
    build-base \
    python3 \
    python3-dev \
    # wget dependency
    openssl \
    # dev dependencies
    bash \
    git \
    py3-pip \
    sudo \
    # Pillow dependencies
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev \
    zbar-dev && \
    pip install -r requirements.txt

COPY runserver.py ./
COPY sathub ./sathub
COPY config-sathub.json ./
COPY dll ./dll


CMD python runserver.py 
