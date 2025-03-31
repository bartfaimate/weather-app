import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound


from pathlib import Path
import sys

sys.path.append(Path(__file__).resolve().parents[1].as_posix())

from models.weather_entries import WeatherData
from query_handlers.weather_queries import WeatherQueries



# Create a test database
engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)

def setup_function():
    WeatherData.metadata.create_all(engine)

def teardown_function():
    WeatherData.metadata.drop_all(engine)

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.close()

@pytest.fixture
def weather_queries(db_session):
    return WeatherQueries(db_session)

def test_get_weather_all(weather_queries, db_session):
    entry = WeatherData(id="1", temperature=25.0, humidity=50.0, location="Test place", timestamp=datetime.now())
    db_session.add(entry)
    db_session.commit()
    
    results = weather_queries.get_weather_all()
    assert len(results) == 1
    assert results[0].temperature == 25.0


def test_get_weather_by_id(weather_queries, db_session):
    entry = WeatherData(id="1", temperature=25.0, humidity=50.0, location="Test place", timestamp=datetime.now())
    db_session.add(entry)
    db_session.commit()
    
    result = weather_queries.get_weather_by_id("1")
    assert result.location == "Test place"


def test_get_weather_by_id_not_found(weather_queries):
    with pytest.raises(NotFound):
        weather_queries.get_weather_by_id("99")


def test_create_weather_data(weather_queries, db_session):
    entry = weather_queries.create_weather_data(temperature=20.0, humidity=40.0, location="Kitchen")
    assert entry.location == "Kitchen"
    
    result = db_session.query(WeatherData).first()
    assert result is not None
    assert result.temperature == 20.0


def test_update_weather_data(weather_queries, db_session):
    entry = WeatherData(id="1", temperature=22.0, humidity=55.0, location="bed room", timestamp=datetime.now())
    db_session.add(entry)
    db_session.commit()
    
    updated_entry = weather_queries.update_weather_data("1", temperature=30.0)
    assert updated_entry.temperature == 30.0


def test_update_weather_data_not_found(weather_queries):
    with pytest.raises(NotFound):
        weather_queries.update_weather_data("99", temperature=30.0)


def test_delete_weather_data(weather_queries, db_session):
    entry = WeatherData(id="1", temperature=15.0, humidity=60.0, location="Kitchen", timestamp=datetime.now())
    db_session.add(entry)
    db_session.commit()
    
    weather_queries.delete_weather_data("1")
    db_session.commit()
    
    result = db_session.query(WeatherData).filter_by(id="1").first()
    assert result is None


def test_validate_temperature():
    from query_handlers.weather_queries import validate_temperature
    
    with pytest.raises(BadRequest):
        validate_temperature(-100)
    with pytest.raises(BadRequest):
        validate_temperature(200)
    validate_temperature(25)  # Should not raise an error


def test_validate_humidity():
    from query_handlers.weather_queries import validate_humidity
    
    with pytest.raises(BadRequest):
        validate_humidity(-10)
    with pytest.raises(BadRequest):
        validate_humidity(150)
    validate_humidity(50)  # Should not raise an error
