FROM python:3.6-alpine3.7

RUN apk update && apk upgrade
RUN apk add --no-cache bash git openssh
RUN apk add --no-cache python3-dev
RUN apk add --no-cache --virtual .build-deps g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

WORKDIR /usr/src/app

COPY . .

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/iobis/pyxylookup.git#egg=pyxylookup

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "gunicorn.conf", "--log-config", "logging.conf", "-b", ":8000", "service.app:api"]
