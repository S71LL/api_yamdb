from rest_framework import viewsets
from reviews.models import Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


class CategotyViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    # serializer_class
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
