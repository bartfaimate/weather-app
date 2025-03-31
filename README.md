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


## Development:
Development machine: Mac with apple silicon.

Docker is required

```bash
cd /path/to/weather-app
docker compose up --build -d mssql backend weather-app
```

After services are up the frontend can accessed on `http://localhost:8080`
and the API under `http://localhost:5001`
## Testing:
```bash 
cd backend
pytest tests/

## Deployement:

## Further development:
* Enhance UI
    * Add dashboard with graphics. 
