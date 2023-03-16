from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategotyViewSets

router = SimpleRouter()
router.register(r'category', CategotyViewSets)

urlpatterns = [
    path('', include('routers.urls'))
]
