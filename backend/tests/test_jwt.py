import pytest
import time
import json
from jwcrypto import jwt, jwk
from werkzeug.exceptions import Unauthorized
from pathlib import Path

import sys
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
print(sys.path, flush=True)

from utils.jwt import Jwt  # Adjust import based on actual file structure

def test_create_key():
    key = Jwt.create_key()
    assert isinstance(key, jwk.JWK)

def test_save_and_load_key(tmp_path):
    key = Jwt.create_key()
    key_path = tmp_path / "jwt.key"
    Jwt.save_key_to_file(key, key_path)
    loaded_key = Jwt.load_key_from_file(key_path)
    assert key.export() == loaded_key.export()

def test_create_signed_token():
    key = Jwt.create_key()
    data = {"user": "test", "role": "admin"}
    token = Jwt.create_signed_token(data, key)
    assert isinstance(token, jwt.JWT)

def test_parse_token():
    key = Jwt.create_key()
    data = {"user": "test"}
    token = Jwt.create_signed_token(data, key)
    parsed_data = Jwt.parse_token(key, token.serialize())
    assert parsed_data == data

def test_encrypt_decrypt_token():
    key = Jwt.create_key()
    data = {"user": "test"}
    token = Jwt.create_signed_token(data, key)
    encrypted_token = Jwt.encrypt_token(token, key)
    decrypted_data = Jwt.decrypt_token(key, encrypted_token.serialize())
    assert decrypted_data == data


if __name__ == "__main__":
    pytest.main()
