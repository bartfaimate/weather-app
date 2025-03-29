
from __future__ import annotations
from functools import wraps
import logging
from collections.abc import Callable
from utils.jwt import Jwt
from werkzeug.exceptions import Unauthorized
from flask import request

log = logging.getLogger("routes.py")
log.setLevel(logging.DEBUG)


JWT_KEY = "jwt_key"

def login_required(func:Callable) -> Callable:
    """Decorator for login"""
    # func is sync
    
    @wraps(func)
    def wrap(*args, **kwargs):
        if not (token := request.headers.get("Authorization")):
            raise Unauthorized("Login is required")
        log.debug(f"Wrapping {token} with login_required")
        token = token.split("Bearer ")[1]
        key = Jwt.load_key_from_file()
        decrypted_data = Jwt.decrypt_and_verify_expired(key=key, token=token, expiration=5 * 3600)
        if not (user_id := decrypted_data.get("user_id")):
            raise Unauthorized("Missing user_id")

        return  func(*args, **kwargs)

    return wrap