from __future__ import annotations
from typing import List, Optional
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from dataclasses import dataclass
from uuid import uuid4

from models.base import Base

from sqlalchemy import Table, ForeignKey



from typing import Literal, TYPE_CHECKING


# "admin" | "user" | "owner"

@dataclass
class User(Base):
    __tablename__ = 'users'

    id : Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=sqlalchemy.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())

    

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
        }

