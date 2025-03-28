from sqlalchemy import create_engine
import os
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, database_url: str):
        self.url = database_url
        self.engine = create_engine(database_url)

    def create_all(self):
        from models.base import Base
        print("Creating tables", flush=True)
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        from models.base import Base
        Base.metadata.drop_all(self.engine)

    def get_engine(self):
        return self.engine
    
    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
    

DATABASE_URL = f"mssql+pyodbc://{os.getenv('SQL_USER', 'sa')}:{os.getenv('SQL_PASSWORD', 'Password_1234')}@mssql_container:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

database = Database(DATABASE_URL)

print(f"Database initialised: {database.url}", flush=True)

@contextmanager
def get_db():
    Session = sessionmaker(bind=database.engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()