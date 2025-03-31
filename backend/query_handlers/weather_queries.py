from __future__ import annotations

from datetime import datetime

from models.weather_entries import WeatherData
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import delete, select
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized


class WeatherQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_all(self) -> list[WeatherData]:
        entries = self.db.execute(select(WeatherData)).scalars().all()
        return entries

    def get_weather_by_id(self, weather_id: str) -> WeatherData:
        entry = (
            self.db.execute(select(WeatherData).where(WeatherData.id == weather_id))
            .scalars()
            .one_or_none()
        )

        if not entry:
            raise NotFound(f"entry not found")
        return entry

    def create_weather_data(
        self,
        temperature: float,
        humidity: float,
        location: str,
        timestamp: datetime | None = None,
        **kwargs,
    ) -> WeatherData:
        
        temperature and validate_temperature(temperature)
        humidity and validate_humidity(humidity)

        entry = WeatherData(
            temperature=temperature,
            humidity=humidity,
            location=location,
            timestamp=timestamp or datetime.now(),
        )
        self.db.add(entry)
        self.db.commit()

        return entry

    def update_weather_data(
        self,
        weather_id: str,
        temperature: float | None = None,
        humidity: float | None = None,
        timestamp: datetime | None = None,
        location: str | None = None,
        **kwargs,
    ) -> WeatherData:
        temperature and validate_temperature(temperature)
        humidity and validate_humidity(humidity)

        entry = self.get_weather_by_id(weather_id)
        entry.timestamp = timestamp or entry.timestamp
        entry.humidity = humidity or entry.humidity
        entry.temperature = temperature or entry.temperature
        entry.location = location or entry.location
        self.db.commit()
        return entry

    def delete_weather_data(self, weather_id: str):
        self.db.execute(delete(WeatherData).where(WeatherData.id == weather_id))
        self.db.commit()



def validate_args(**kwargs):
    required = {"humidity", "temperature", "location"}
    if required.intersection(set(kwargs)) != required:
        raise BadRequest(f" {list(required)} should be in the body")


def validate_temperature(temperature):
    if  not isinstance(temperature, (float, int)) or temperature < -80 or temperature > 80:
        raise BadRequest("'temperature' is in Celsius, it should be between -80 and 80")


def validate_humidity(humidity):
    if not isinstance(humidity, (float, int)) or humidity < 0 or humidity > 100:
        raise BadRequest("'humidity' should be between 0 and 100")
