# Weather-app

## Use-case: 

* The Application runs on a home server. For example on a Raspberry pi
* There are some IOT devices in the house / flat 
* These measure the humidity and temperature and put data into the weather app via HTTP requests

* Everyone can view the temperature data on a dashboard
* Specified person (admin) can update, delete, create manually data if needed


## Structure of project:
There are 3 services running in a docker compose
* Database (mssql)
* backend (backend)
* weather-app (frontend)


Here is an image of the structure and usage: [image](weather-app-diagram.jpg)


The backend (Flask) related files are in the backend folder
* /models -> SqlAlchemy models
* /routers -> api endpoint blueprints
* /query_handlers -> sql handlers
* /middleware -> just the login validator is there
* /database -> session and DB engine related logic
* /tests -> unit tests
* /utils -> jwt creation and validation is located

The API documentation can be found here: [openapi.yml](backend/openapi.yaml)

Frontend (weather-app) related files:
* /src/view -> contains react pages
* /src/modules -> react reusable components/modules

## Development:
Development machine was: Mac with apple silicon. (Should be platform independent)

Docker is required

```bash
cd /path/to/weather-app/.dev
docker compose up --build -d mssql backend weather-app
```

After services are up the frontend can be accessed on `http://localhost:8080`
and the API under `http://localhost:5001`

## Testing:
You can run unittests locally, but you have to install the backend/requirements.txt in a virtualenvironment.

```bash 
cd backend
pytest tests/
```


# Further development:
* Enhance UI
    * Add dashboard with graphics. 
    * handle logout
* API:
    * get a refresh token after each request
* Add CI/CD pipeline. Run tests on push, automatic deployement
* enable debugging for backend