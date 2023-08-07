import datetime
import jwt

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from blog.services.exceptions import InvalidJWTException


def is_auth_token_valid(auth_token):
    _ = auth_token[:7] if auth_token else ''
    return _ == 'Bearer '


def get_decoded_jwt_token(jwt_key):
    try:
        return jwt.decode(jwt_key, settings.SECRET_KEY, algorithms='HS256')
    except jwt.exceptions.InvalidTokenError or jwt.exceptions.DecodeError:
        raise InvalidJWTException('Invalid token')
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidJWTException('The token is expired')


def generate_tokens(user: User):
    access_exp_time = datetime.datetime.today() + datetime.timedelta(days=7)
    refresh_exp_time = access_exp_time + datetime.timedelta(days=23)
    decoded_user = {
        'name': user.username,
        'email': user.email,
        'groups': [group.name for group in user.groups.all()],
        'sub': user.id,
        'typ': 'access',
        'exp': datetime.datetime.fromisoformat(access_exp_time.isoformat()).timestamp()
    }
    decoded_refresh = {
        'typ': 'refresh',
        'sub': user.id,
        'exp': datetime.datetime.fromisoformat(refresh_exp_time.isoformat()).timestamp()
    }
    access_token = jwt.encode(decoded_user, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(decoded_refresh, settings.SECRET_KEY, algorithm='HS256')
    return access_token, refresh_token


def refresh_access_token(token):
    payload = get_decoded_jwt_token(token)
    if payload.get('typ') == 'refresh':
        try:
            return generate_tokens(User.objects.get(id=payload.get('sub')))
        except ObjectDoesNotExist:
            pass
    raise InvalidJWTException('Refresh token is not valid')


def verify_token(token):
    payload = get_decoded_jwt_token(token)
    try:
        return User.objects.get(id=payload.get('sub'))
    except ObjectDoesNotExist:
        return None
