

from __future__ import annotations
from typing import List, Optional
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from dataclasses import dataclass
from uuid import uuid4

from models.base import Base

from sqlalchemy import Table, ForeignKey


from typing import Literal, TYPE_CHECKING

OVERCAST = Literal["cloudy", "clear", "partially_cloudy", "fog", "N/A"]

@dataclass
class WeatherData(Base):
    __tablename__ = 'weather_data'

    id : Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), primary_key=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True) # celsius
    sky_overcast: Mapped[OVERCAST] = mapped_column(String(64), default="N/A")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=sqlalchemy.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

    def __repr__(self):
        return f'<WeatherData {self.temperature} {self.sky_overcast}>'

    def to_dict(self):
        return {
            "id": self.id,
            "temperature": self.temperature,
            "sky_overcast": self.sky_overcast,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

