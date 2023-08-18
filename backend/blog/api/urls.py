from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'reports', ReportViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('get-token', AuthAPIView.as_view()),
    path('refresh-token', RefreshTokenAPIView.as_view()),
    path('very-token', TokenVerificationView.as_view())
]
