import jwt

from django.conf import settings

from blog.services.exceptions import InvalidJWTException


def is_auth_token_valid(auth_token):
    _ = auth_token[:7] if auth_token else ''
    return _ == 'Bearer '


def get_decoded_jwt_user(jwt_key):
    try:
        return jwt.decode(jwt_key, settings.SECRET_KEY, algorithms='HS256')
    except jwt.exceptions.InvalidTokenError or jwt.exceptions.DecodeError:
        raise InvalidJWTException('Invalid token')
