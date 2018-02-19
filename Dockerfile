FROM python:3.6-alpine3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":8000", "service.app:api"]