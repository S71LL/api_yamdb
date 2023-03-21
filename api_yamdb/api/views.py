from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from titles.models import Title, Review, Category
from users.models import JWTToken
from .serializers import (CategorySerializer,
                          TitleSerializer,
                          SignupSerializer,
                          AdminUserSerializer,
                          UserMeSerializer,
                          UserTokenSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          GenreSerializer)
from .permissions import AuthorOrReadOnly, IsAdmin, IsModerator
from .core.utils import generate_code


User = get_user_model()


class TitleViewSets(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    permission_classes = (IsAdmin, )
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin, )
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly, IsAdmin, IsModerator)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class GenreViewSets(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin, )
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    """Создание, редактирование и удаление пользователя администратором."""
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)


class UserMeViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    """Самостоятельное получение и обновление данных о пользователе."""
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save(partial=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PATCH', 'PUT'])
@permission_classes(permission_classes=[AllowAny])
def sign_up(request):
    """
    Самостоятельная регистрация новых пользователей и получение кода на почту.
    """
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.validated_data['email']
            code = generate_code()
            msg = ('Привет! Воспользуйся, пожалуйста, '
                   f'этим кодом для регистрации {code}')
            send_mail(
                subject='Код для регистрации',
                message=msg,
                from_email='example@mail.ru',
                recipient_list=[to_email],
                fail_silently=False
            )
            serializer.save(confirmation_code=code)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH' or 'PUT':
        username = request.data['username']
        to_email = request.data['email']
        user = get_object_or_404(User, username=username)
        serializer = SignupSerializer(instance=user, data=request.data)
        if user.email != to_email:
            msg = {
                'email':
                [
                    'Введен неверный адрес электронной почты. '
                    'Проверь данные или зарегистрируйся.'
                ]
            }
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            code = generate_code()
            msg = ('Привет! Воспользуйся, пожалуйста, '
                   f'этим кодом для получения нового токена {code}')
            send_mail(
                subject='Код для получения токена',
                message=msg,
                from_email='example@mail.ru',
                recipient_list=[to_email],
                fail_silently=False
            )
            user.confirmation_code = code
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(permission_classes=[AllowAny])
def token_obtain(request):
    """Получение токена пользователем."""
    if request.method == 'POST':
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        serializer = UserTokenSerializer(
            instance=user, data=request.data)
        code = user.confirmation_code
        if code != request.data['confirmation_code']:
            msg = {'confirmation_code': 'Введен неверный код =('}
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            token_pair = RefreshToken.for_user(user)
            JWTToken.objects.create(
                key=str(token_pair.access_token), user=user)
            user.confirmation_code = ''
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
