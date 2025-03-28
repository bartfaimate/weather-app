from __future__ import annotations

from datetime import datetime

from models.types import OVERCAST_TYPE
from models.users import User
from models.weather_entries import WeatherData
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import delete, select
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash, generate_password_hash


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
        sky_overcast: OVERCAST_TYPE,
        timestamp: datetime | None = None,
        **kwargs,
    ) -> WeatherData:
        temperature and validate_temperature(temperature)
        sky_overcast and validate_overcast(sky_overcast)

        entry = WeatherData(
            temperature=temperature,
            sky_overcast=sky_overcast,
            timestamp=timestamp or datetime.now(),
        )
        self.db.add(entry)
        self.db.commit()

        return entry

    def update_weather_data(
        self,
        weather_id: str,
        temperature: float | None = None,
        sky_overcast: OVERCAST_TYPE | None = None,
        timestamp: datetime | None = None,
        **kwargs,
    ) -> WeatherData:
        temperature and validate_temperature(temperature)
        sky_overcast and validate_overcast(sky_overcast)

        entry = self.get_weather_by_id(weather_id)
        entry.timestamp = timestamp or entry.timestamp
        entry.sky_overcast = sky_overcast or entry.sky_overcast
        entry.temperature = temperature or entry.temperature
        self.db.commit()
        return entry

    def delete_weather_data(self, weather_id: str):
        self.db.execute(delete(WeatherData).where(WeatherData.id == weather_id))


def validate_args(**kwargs):
    required = {"sky_overcast", "temperature"}
    if required.intersection(set(kwargs)) != required:
        raise BadRequest(f" {list(required)} should be in the body")


def validate_temperature(temperature):
    if temperature < -80 or temperature > 80:
        raise BadRequest("'temperature' is in Celsius, it should be between -80 and 80")


def validate_overcast(sky_overcast):
    if sky_overcast not in list(OVERCAST_TYPE.__args__):
        raise BadRequest(f"'sky_overcast' should be in {list(OVERCAST_TYPE.__args__)}")
