from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSets, ReviewViewSet, CommentViewSet

router = SimpleRouter()
router.register(r'category', CategoryViewSets)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register(r'titles/(?P<title_id>\d+)'
                r'/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('', include(router.urls)),
]
