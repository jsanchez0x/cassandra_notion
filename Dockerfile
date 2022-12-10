FROM alpine:latest

ENV CASSANDRA_HOME=/cassandra
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk upgrade \
    && apk add --no-cache \
    python3 \
    tzdata

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
    echo "Europe/Madrid" > /etc/timezone && \
    apk del tzdata

COPY ./app $CASSANDRA_HOME

RUN ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r $CASSANDRA_HOME/requirements.txt

COPY ./bin /usr/local/bin
RUN chmod a+x /usr/local/bin/*

COPY ./utils/crontab.txt /crontab.txt
RUN /usr/bin/crontab /crontab.txt

ENTRYPOINT ["init_container"]