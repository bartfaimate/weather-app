import functools
from sqlalchemy import select
from flask import (
    Blueprint, jsonify, request, Response
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

from database.database import get_db
from models.users import User
# from middleware.login_validator import login_required
from utils.jwt import Jwt
from werkzeug.exceptions import BadRequest, InternalServerError
from query_handlers.user_queries import UserQueries
from query_handlers.weather_queries import WeatherQueries, validate_args

api = Blueprint('app', __name__, url_prefix='/api/')

CORS(api)
# CORS(api, resources={r"/ask": {"origins": "http://localhost:9090"}})

@api.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

@api.get('/weather/')
def get_all_weather_data():
    with get_db() as db:
        entries = WeatherQueries(db).get_weather_all()
    
        res = [entry.to_dict() for entry in entries]
        return jsonify(res)

@api.get('/weather/<string:weather_id>/')
def get_weather_data(weather_id:str):
    with get_db() as db:
        entry = WeatherQueries(db).get_weather_by_id(weather_id)
        return jsonify(entry.to_dict())

@api.post('/weather/')
def create_weather_data():
    data = request.json
    validate_args(**data)
    with get_db() as db:
        entry = WeatherQueries(db).create_weather_data(**data)
        return jsonify(entry.to_dict())

@api.put('/weather/<string:weather_id>/')
def update_weather_data(weather_id:str):
    data = request.json
    with get_db() as db:
        entry = WeatherQueries(db).update_weather_data(weather_id=weather_id, **data)
        return jsonify(entry.to_dict())

@api.delete('/weather/<string:weather_id>/')
def delete_weather_data(weather_id:str):
     with get_db() as db:
        WeatherQueries(db).delete_weather_data(weather_id=weather_id)
        return jsonify("ok")



@api.post('/user/register/')
def register_user():
    data = request.json
    required = {"email", "password"}
    if required.intersection(set(data)) != required:
        raise BadRequest(f" {list(required)} fields must be in the body")
    
    with get_db() as db:
        try:
            user: User = UserQueries(db).register_user(**data)
        except Exception as e:
            raise InternalServerError(e)

        return jsonify(user.to_dict())


@api.post('/user/login/')
def login_user():
    data = request.json
    required = {"email", "password"}

    if required.intersection(set(data)) != required:
        raise BadRequest(f" {list(required)} fields must be in the body")
    
    with get_db() as db:
        user = UserQueries(db).get_user_by_email(data["email"])
        if not user:
            return jsonify({'message': 'User with this email does not exists'}), 401
        if not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        resp_dict = user.to_dict()
        resp_dict["user_id"] = user.id

        key = Jwt.load_key_from_file()
        token = Jwt.create_token_with_timestamp(resp_dict, key)

        token = Jwt.encrypt_token(token, key).serialize()
        resp_dict.update({"jwt": token})

        return jsonify(resp_dict)

