from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User


class UserQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email) -> User:
        try:
            user: User = (
                self.db.execute(select(User).where(User.email == email))
                .scalars()
                .one_or_none()
            )
            print(user, flush=True)
            return user
        except OperationalError as e:
            print(e, flush=True)
            raise NotFound("User not found")

    def get_user_by_id(self, user_id) -> User:
        try:
            user: User = (
                self.db.execute(select(User).where(User.id == user_id))
                .scalars()
                .one_or_none()
            )
        except OperationalError as e:
            raise NotFound("User not found")
        return user

    def register_user(self, email: str, password: str, **kwargs) -> User:
        user = self.get_user_by_email(email)
        if user:
            raise BadRequest(f"This user already exists {user}")

        try:
            password = generate_password_hash(password)
            entry = User(email=email, password=password)
            self.db.add(entry)
            self.db.commit()
            return entry
        except SQLAlchemyError as e:
            raise BadRequest(f"This user already exists {e}")
        except Exception as e:
            raise BadRequest(f"Data is missing {e}")
