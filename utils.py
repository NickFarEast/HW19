import base64
import hashlib
from flask_restx import abort
from flask import request, current_app
import jwt
from datetime import datetime, timedelta
import constant
from typing import Dict


def get_hash_password(password: str) -> str:
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        constant.PWD_HASH_SALT,
        constant.PWD_HASH_ITERATIONS
    )).decode('utf-8')


def generate_tokens(data: dict) -> Dict[str, str]:
    data['exp'] = datetime.utcnow() + timedelta(minutes=30)
    data['refresh_token'] = False

    access_token: str = jwt.encode(
        payload=data,
        key=constant.SECRET_KEY,
        algorithm=constant.JWT_ALGORITHM
    )

    data['exp'] = datetime.utcnow() + timedelta(days=30)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=constant.SECRET_KEY,
        algorithm=constant.JWT_ALGORITHM
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_token_from_headers(headers: dict):
    if 'Authorization' not in request.headers:
        abort(401)

    return headers['Authorization'].split('Bearer ')[-1]


def decode_token(token: str, refresh_token=False):
    decoded_token = {}

    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=constant.SECRET_KEY,
            algorithms=[constant.JWT_ALGORITHM])
    except jwt.PyJWTError:
        current_app.logger.info('Got wrong token:"%s"', token)
        abort(401)

    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='Got wrong token type.')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):
        token = get_token_from_headers(request.headers)
        decode_token(token)

        return func(*args, **kwargs)

    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):
        token = get_token_from_headers(request.headers)
        decoded_token = decode_token(token)
        print(decoded_token)
        if decoded_token.get('role') != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
