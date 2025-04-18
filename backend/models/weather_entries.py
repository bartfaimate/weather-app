

from __future__ import annotations
from typing import List, Optional
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from dataclasses import dataclass
from uuid import uuid4
from typing import Literal, TYPE_CHECKING
from sqlalchemy import Table, ForeignKey
from datetime import datetime
from models.base import Base
from models.types import OVERCAST_TYPE


@dataclass
class WeatherData(Base):
    __tablename__ = 'weather_data'

    id : Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), primary_key=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True) # celsius
    humidity: Mapped[float] = mapped_column(Float, nullable=True) # percentage
    location: Mapped[str] = mapped_column(String(128))
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=sqlalchemy.func.now())

    def __repr__(self):
        return f'<WeatherData {self.temperature} {self.humidity} {self.location}>'

    def to_dict(self):
        return {
            "id": self.id,
            "temperature": self.temperature,
            "timestamp": self.timestamp,
            "location": self.location,
            "humidity": self.humidity,
        }

