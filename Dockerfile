# Dockerfile for deployment to Heroku

FROM node:lts-alpine3.13 as build-react
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./animal_adoption/front_end/package.json ./
COPY ./animal_adoption/front_end/package-lock.json ./
RUN npm ci -- silent
COPY ./animal_adoption/front_end ./
RUN npm run build

FROM python:3.9.4
RUN apt-get update -y
RUN apt-get install -y vim
RUN mkdir -p /var/www/animal_adoption
WORKDIR /var/www/animal_adoption
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . ./
COPY --from=build-react /app/build /var/www/animal_adoption/animal_adoption/front_end/build
# env variables
ENV ENV=prod
ENV PYTHONPATH=.
# run server
CMD gunicorn --workers=2 --bind 0.0.0.0:${PORT} animal_adoption.run:app
