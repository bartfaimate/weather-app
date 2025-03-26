from sqlalchemy import create_engine
import os
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, database_url: str):
        self.url = database_url
        self.engine = create_engine(database_url)

    def create_all(self):
        from backend.models.base import Base
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        from backend.models.base import Base
        Base.metadata.drop_all(self.engine)

    def get_engine(self):
        return self.engine
    
    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
    

DATABASE_URL = f"mssql+pyodbc://sa:{os.getenv('SQL_PASSWORD')}@mssql:1433/master?driver=ODBC+Driver+17+for+SQL+Server"


database = Database(f"mssql+pyodbc://user:password@server/database")

print(f"Database initialised: {database.url}")
@contextmanager
def get_db():
    Session = sessionmaker(bind=database.engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()