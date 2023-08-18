from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.services.auth import generate_tokens, refresh_access_token, verify_token
from blog.api.serializers import *
from blog.services.exceptions import InvalidJWTException
from django.contrib.auth import authenticate
from blog.services.permissions import ReadOnlyJWTPermission


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyJWTPermission]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ['post']

# @api_view(['POST'])
# def auth_user(request):
class AuthAPIView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                access_token, refresh_token = generate_tokens(user)
                response = Response(data={'access_token': access_token, 'refresh_token': refresh_token})
                response.set_cookie('access_token', access_token)
                response.set_cookie('refresh_token', refresh_token)
                return response
            return Response(data={'detail': 'Username or password is not correct'}, status=403)
        return Response(data={'detail': serializer.errors}, status=400)


class RefreshTokenAPIView(APIView):
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh_token']
            try:
                access_token, _ = refresh_access_token(refresh_token)
                response = Response(data={'access_token': access_token})
                response.set_cookie('access_token', access_token)
                return response
            except InvalidJWTException as e:
                return Response({'detail': e.message}, status=403)
        return Response(data={'detail': serializer.errors}, status=400)


class TokenVerificationView(APIView):
    def post(self, request):
        serializer = TokenVerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = verify_token(serializer.data['access_token'])
                return Response({'username': user.username})
            except InvalidJWTException as e:
                return Response({'detail': e.message}, status=403)
        return Response(data={'detail': serializer.errors}, status=400)