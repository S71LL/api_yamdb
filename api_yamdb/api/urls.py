from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ReviewViewSet, UserViewSet, UserMeViewSet, sign_up, token_obtain)

from .views import (
    CategoryViewSets, ReviewViewSet, CommentViewSet, GenreViewSets,
    TitleViewSets
)

name = 'api'

router = SimpleRouter()

router.register('titles', TitleViewSets, basename='titles')
router.register('categories', CategoryViewSets)
router.register('genres', GenreViewSets, basename='genres')
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
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
