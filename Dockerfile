FROM python:3.6-alpine3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn json-logging-py

COPY . .

EXPOSE 8000

https://sebest.github.io/post/protips-using-gunicorn-inside-a-docker-image/

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":8000", "app:api"]