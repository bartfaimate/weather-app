from sqlalchemy.orm import declarative_base

Base = declarative_base()

def init_db():
    """Initialize the database and create tables."""
    from database.database import database
    engine = database.get_engine()
    Base.metadata.create_all(bind=engine)