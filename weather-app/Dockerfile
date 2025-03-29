FROM node:23.10-slim AS prod

RUN apt update && apt install curl -y

# COPY ./package-lock.json /weather-app/package-lock.json

WORKDIR /weather-app

COPY ./package.json ./
RUN npm install

CMD ["npm", "run", "dev"]

# FROM prod AS dev
# RUN apt-get update && apt-get install -y nodejs npm
# RUN npm install -g nodemon
# CMD nodemon main.py