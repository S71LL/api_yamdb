from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CategoryViewSets, ReviewViewSet

router = SimpleRouter()
router.register(r'category', CategoryViewSets)
router.register(r'titles/(?P<title_id>\d+)/rewiews',
                ReviewViewSet, basename='review')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('', include(router.urls)),
]
