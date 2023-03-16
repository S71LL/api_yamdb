from rest_framework.decorators import api_view

from .serializers import (
    SignupSerializer, ObtainTokenSerializer, UserSerializer)


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        