FROM python:3.12-slim-bookworm AS prod

RUN apt-get update
RUN apt-get install -y curl gpg \ 
unixodbc \
unixodbc-dev \
odbcinst \
libodbc1 \
&& rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver 18 for SQL Server
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl -fsSL https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*
    
COPY ./requirements.txt /backend/requirements.txt
RUN pip3 install -r /backend/requirements.txt


WORKDIR /backend

CMD ["python", "main.py"]


FROM prod AS dev
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g nodemon
CMD nodemon main.py