from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ReviewViewSet, UserViewSet, UserMeViewSet, sign_up, token_obtain)

from .views import ReviewViewSet, CommentViewSet

name = 'api'

router = SimpleRouter()

router.register(r'titles/(?P<title_id>\d+)/rewiews',
                ReviewViewSet, basename='review')
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)'
                r'/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('auth/signup/', sign_up, name='sign_up'),
    path('auth/token/', token_obtain, name='token_obtain'),
    path(
        'users/me/',
        UserMeViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update'}),
        name='user_me'),
    path('', include(router.urls)),
]
