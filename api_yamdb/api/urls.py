from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ReviewViewSet, UserViewSet, UserMeViewSet, sign_up, token_obtain)

name = 'api'

router = SimpleRouter()

router.register(r'titles/(?P<title_id>\d+)/rewiews',
                ReviewViewSet, basename='review')
router.register(r'users', UserViewSet)
# router.register(r'users/me/', UserMeViewSet, basename='users_me')


urlpatterns = [
    path('auth/signup/', sign_up, name='sign_up'),
    path('auth/token/', token_obtain, name='token_obtain'),
    path(
        'users/me/',
        UserMeViewSet.as_view(
            {'get': 'retrieve', 'put': 'update', 'patch': 'update'}),
        name='user_me'),
    path('', include(router.urls)),
]
