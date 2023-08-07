import json

from django.http import HttpResponse

from blog.services.auth import is_auth_token_valid, get_decoded_jwt_user
from blog.services.exceptions import InvalidJWTException


class OpenIDAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        meta = request.META
        if 'HTTP_AUTHORIZATION' in meta:
            token = meta.get('HTTP_AUTHORIZATION')
            if not is_auth_token_valid(token):
                return HttpResponse(
                    content=json.dumps({'detail': 'invalid token format'}),
                    content_type='application/json',
                    status=400
                )
            token = token[7:]
            try:
                request.jwt_user = get_decoded_jwt_user(token)
            except InvalidJWTException as e:
                return HttpResponse(
                    content=json.dumps({'detail': e.message}),
                    content_type='application/json',
                    status=400
                )
        else:
            request.jwt_user = None
        response = self.get_response(request)
        return response
