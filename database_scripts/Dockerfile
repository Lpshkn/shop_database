FROM ubuntu:latest
MAINTAINER LeadNess

RUN apt-get update \
 && apt-get install -y wget \
 && rm -rf /var/lib/apt/lists/*

# Mssql server keys
RUN apt-get update \
 && apt install -y software-properties-common \
 && apt-get install -y gnupg \
 && wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/18.04/mssql-server-2019.list)"

# Mssql tools keys
RUN apt-get install -y curl \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

RUN apt-get update \
 && apt-get install -y mssql-server

ENV ACCEPT_EULA=Y
RUN apt-get update \
 && echo Yes Yes | apt-get install -y mssql-tools

RUN apt-get update \
 && echo yes yes | apt-get install -y unixodbc-dev

COPY create_tables.sql /create_tables.sql
COPY insert_values.sql /insert_values.sql
COPY entrypoint /entrypoint

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
 && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
 && . ~/.bashrc

RUN apt-get install -y sudo
