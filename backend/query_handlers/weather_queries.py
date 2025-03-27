from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select, delete
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User
from models.weather_entries import WeatherData
from models.types import OVERCAST_TYPE


class WeatherQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_all(self) -> list[WeatherData]:
        try:
            self.db.execute(select(WeatherData)).scalars().all()
        except OperationalError as e:
            raise NotFound("User not found")
        except SQLAlchemyError as e:
            raise BadRequest(f"This user already exists {e}")

    def get_weather_by_id(self, weather_id: str) -> WeatherData:
        try:
            self.db.execute(
                select(WeatherData).where(WeatherData.id == weather_id)
            ).scalars().one_or_none()
        except OperationalError as e:
            raise NotFound("User not found")
        except SQLAlchemyError as e:
            raise BadRequest(f"This user already exists {e}")

    def create_weather_data(
        self,
        temperature: float,
        sky_overcast: OVERCAST_TYPE,
        timestamp: datetime | None = None,
        **kwargs
    ) -> WeatherData:

        if temperature < -80 or temperature > 80:
            raise BadRequest(
                "'temperature' is in Celsius, it should be between -80 and 80"
            )
        if sky_overcast not in OVERCAST_TYPE:
            raise BadRequest(f"'sky_overcast' should be in {list(OVERCAST_TYPE)}")
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
        **kwargs
    ) -> WeatherData:
        if temperature < -80 or temperature > 80:
            raise BadRequest(
                "'temperature' is in Celsius, it should be between -80 and 80"
            )
        if sky_overcast not in OVERCAST_TYPE:
            raise BadRequest(f"'sky_overcast' should be in {list(OVERCAST_TYPE)}")
        entry = self.get_weather_by_id(weather_id)
        entry.timestamp = timestamp or entry.timestamp
        entry.sky_overcast = sky_overcast or entry.sky_overcast
        entry.temperature = temperature or entry.temperature
        self.db.commit()
        return entry

    def delete_weather_data(self, weather_id: str):
        self.db.execute(delete(WeatherData).where(WeatherData.id == weather_id))
