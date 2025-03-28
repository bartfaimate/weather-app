from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Literal, Optional
from uuid import uuid4

import sqlalchemy
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.base import Base

# "admin" | "user" | "owner"


@dataclass
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid4()), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(512), unique=True)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=sqlalchemy.func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()
    )

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
        }
