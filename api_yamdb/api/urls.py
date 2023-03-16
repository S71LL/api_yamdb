from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet

router = DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/rewiews',
                ReviewViewSet, basename='review')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('', include(router.urls)),
]
