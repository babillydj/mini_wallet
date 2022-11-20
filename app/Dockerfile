# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#ARG CACHE_DATE=2022-01-01
#RUN echo 'hello'

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /src/app/entrypoint.sh
RUN chmod +x /src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/src/app/entrypoint.sh"]
