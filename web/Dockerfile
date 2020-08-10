FROM snakepacker/python:all as builder
MAINTAINER LeadNess

COPY requirements.txt /mnt/
RUN apt-get update \
 && apt-get install -y tdsodbc unixodbc-dev \
 && apt-get clean -y

RUN python3.7 -m venv /usr/share/python3/venv \
 && /usr/share/python3/venv/bin/pip install -U pip \
 && /usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt


RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/arm-linux-gnueabi/odbc/libtdsodbc.so\n\
Setup = /usr/lib/arm-linux-gnueabi/odbc/libtdsS.so" >> /etc/odbcinst.ini

FROM snakepacker/python:3.7 as base

COPY --from=builder /usr/share/python3/venv /usr/share/python3/venv
COPY . /usr/share/python3/

COPY deploy/entrypoint /entrypoint
ENTRYPOINT ["/entrypoint"]