from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet

router = SimpleRouter()

router.register(r'titles/(?P<title_id>\d+)/rewiews',
                ReviewViewSet, basename='review')

urlpatterns = [
    path('auth/signup/', sign_up, name='sign_up'),
    path('auth/token/', token_obtain, name='token_obtain'),
    path('', include(router.urls)),
]
