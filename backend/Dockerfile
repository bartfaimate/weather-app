FROM python:3.12-slim-bookworm as prod

RUN apt-get update
RUN apt-get install -y curl gpg

COPY ./requirements.txt /backend/requirements.txt
RUN pip3 install -r /backend/requirements.txt


WORKDIR /backend

CMD ["python", "main.py"]


FROM prod AS dev
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g nodemon
CMD nodemon main.py