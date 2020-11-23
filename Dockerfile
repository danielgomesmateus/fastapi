FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/code

WORKDIR /app/code/

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
python3-dev postgresql python-psycopg2 libpq-dev

RUN pip3 install --upgrade pip

COPY app/requeriments.txt /app/code/

RUN pip3 install -r /app/code/requeriments.txt

ADD . /app/code/

RUN chmod a+x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]