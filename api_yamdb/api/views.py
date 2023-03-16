from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from titles.models import Title
from .serializers import (
    SignupSerializer, ObtainTokenSerializer, UserSerializer, ReviewSerializer)
from .permissions import AuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
