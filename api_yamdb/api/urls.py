from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSets

router = SimpleRouter()
router.register(r'category', CategoryViewSets)

urlpatterns = [
    path('', include('routers.urls'))
]
