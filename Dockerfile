FROM python:3.8-alpine

RUN adduser -D sathub

WORKDIR /home/sathub

COPY ./requirements/base.txt requirements.txt

COPY ./dll/sat.ini /var/tanca_jetway/sat.ini
COPY ./dll/libsat_v3_0_0_3_x64.so /opt/tanca/libsat_v3_0_0_3_x64.so

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

RUN chown -R sathub:sathub ./

USER sathub

CMD python runserver.py 
