from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import (Title,
                            Review,
                            Category,
                            Genre)
from users.models import User
from .serializers import (CategorySerializer,
                          TitleSerializer,
                          SignupSerializer,
                          AdminUserSerializer,
                          UserMeSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          GenreSerializer)
from .permissions import (IsAuthorModeratorAdminOrReadOnly,
                          IsAdmin,
                          IsAdminOrRead,
                          IsAdminOrGetList)
from .filters import TitleFilter


class UniversalViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                       viewsets.GenericViewSet):
    pass


class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrGetList,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        if request.method == 'GET':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class TitleViewSets(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrRead,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = Review.objects.get(id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review, title=title)


class GenreViewSets(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrGetList,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        if request.method == 'GET':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """Создание, редактирование и удаление пользователя."""
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = r'[\w.@+-]+'

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        methods=['get', 'patch'], detail=False, url_path='me',
        permission_classes=(IsAuthenticated,))
    def users_me(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(
            instance=request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes(permission_classes=[AllowAny])
def sign_up(request):
    """
    Самостоятельная регистрация новых пользователей и получение кода на почту.
    """
    username = request.data.get('username')
    user_exists = User.objects.filter(username=username).exists()
    if not user_exists:
        serializer = SignupSerializer(data=request.data)
    else:
        user = get_object_or_404(User, username=username)
        serializer = SignupSerializer(instance=user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes(permission_classes=[AllowAny])
def token_obtain(request):
    """Получение токена пользователем."""
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if not username or not confirmation_code:
        msg = {
            'username':
            'Поле username обязательно для заполнения',
            'confirmation_code':
            'Поле confirmation code обязательно для заполнения.'} 
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        msg = {'confirmation_code': 'Введен неверный код =('}
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    token_pair = RefreshToken.for_user(user)
    user.token = str(token_pair.access_token)
    user.confirmation_code = ''
    return Response(data={'token': user.token}, status=status.HTTP_200_OK)
