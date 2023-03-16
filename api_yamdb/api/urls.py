from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet


router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/rewiews',
                ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
