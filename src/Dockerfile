FROM python:alpine3.7

COPY . /app

WORKDIR /app

RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
    
EXPOSE 8000

ENV DB_ADDRESS 192.168.203.236
ENV DB_PORT 32408

CMD python3 ./app.py