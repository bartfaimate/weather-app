
import time
import json
from pathlib import Path
from jwcrypto import jwt, jwk
from werkzeug.exceptions import Unauthorized

import logging

log = logging.getLogger(__file__)

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


class Jwt:
    CREATED = "JWT_CREATED_AT"

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_key() -> jwk.JWK:
        return jwk.JWK(generate="oct", size=256)

    @staticmethod
    def save_key_to_file(key: jwk.JWK, dest: str | Path = "/tmp/jwt.key") -> None:
        dest = dest if isinstance(dest, Path) else Path(dest)
        if dest.exists():
            raise OSError("Keyfile exists already. Decide what you want to do")
        with dest.open("w") as fp:
            dest.write_text(key.export())

    @staticmethod
    def load_key_from_file(dest: str | Path = "/tmp/jwt.key") -> jwk.JWK:
        dest = dest if isinstance(dest, Path) else Path(dest)
        if not dest.exists():
            raise OSError("No keyfile exists. Please first create a keyfile with key")
        with dest.open("r") as fp:
            content = dest.read_text().strip()

        return Jwt.load_key(content)

    @staticmethod
    def load_key(key: dict | str) -> jwk.JWK:
        key = json.loads(key) if isinstance(key, str) else key
        return jwk.JWK(**key)

    @staticmethod
    def create_signed_token(data: dict, key: jwk.JWK | str | dict) -> jwt.JWT:
        key = Jwt.load_key(key) if not isinstance(key, jwk.JWK) else key

        try:
            token = jwt.JWT(header={"alg": "HS256"}, claims=data)
        except TypeError:
            for k, v in data.items():
                if not is_jsonable(v):
                    data[k] = str(v)
            token = jwt.JWT(header={"alg": "HS256"}, claims=data)

        token.make_signed_token(key)
        return token

    @staticmethod
    def create_token_with_timestamp(data: dict, key: jwk.JWK | str | dict) -> jwt.JWT:
        data.update({Jwt.CREATED: int(time.time())})

        return Jwt.create_signed_token(data, key)

    @staticmethod
    def encrypt_token(token: jwt.JWT, key: jwk.JWK) -> jwt.JWT:
        encrypted_token = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=token.serialize())
        encrypted_token.make_encrypted_token(key)
        return encrypted_token

    @staticmethod
    def decrypt_and_verify_expired(key: str, token: str, expiration: int = 3600) -> dict:
        data = Jwt.decrypt_token(key, token)
        if Jwt.CREATED not in data:
            raise Unauthorized("No valid token was found")
        if data[Jwt.CREATED] + expiration < time.time():
            raise Unauthorized("Token expired")

        return data

    @staticmethod
    def parse_token(key: jwk.JWK, token: str) -> dict:
        """
        token is not encrypted
        """
        key = Jwt.load_key(key) if not isinstance(key, jwk.JWK) else key
        ET = jwt.JWT(key=key, jwt=token)
        return json.loads(ET.claims)

    @staticmethod
    def decrypt_token(key: jwk.JWK, token: str) -> dict:
        """
        token should be a serialized token and encrypted
        """
        key = Jwt.load_key(key) if not isinstance(key, jwk.JWK) else key
        ET = jwt.JWT(key=key, jwt=token, expected_type="JWE")
        ST = jwt.JWT(key=key, jwt=ET.claims)
        return json.loads(ST.claims)
