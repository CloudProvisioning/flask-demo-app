FROM python:alpine3.7

COPY . /app

WORKDIR /app

RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# RUN python3 -m pip install -r requirements.txt --no-cache-dir
    
EXPOSE 8000

CMD python3 ./app.py