from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('auth/signup/', sign_up, name='sign_up'),
    path('auth/token/', token_obtain, name='token_obtain'),
    path('', include(router.urls)),
]
