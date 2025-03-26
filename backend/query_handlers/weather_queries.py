from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User
from models.weather_entries import WeatherData


class UserQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_all(self) -> list[WeatherData]:
        try:
            self.db.execute(select(WeatherData)).scalars().all()
        except OperationalError as e:
            raise NotFound("User not found")
        except SQLAlchemyError as e:
            raise BadRequest(f"This user already exists {e}")

    def get_weather_by_id(self, weahter_id) -> WeatherData:
        try:
            self.db.execute(
                select(WeatherData).where(WeatherData.id == weahter_id)
            ).scalars().one_or_none()
        except OperationalError as e:
            raise NotFound("User not found")
        except SQLAlchemyError as e:
            raise BadRequest(f"This user already exists {e}")
