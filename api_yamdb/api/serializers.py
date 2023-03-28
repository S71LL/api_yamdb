import re
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import HiddenField
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from reviews.models import Review, Comment, Title, Category, Genre, TitleGenre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = GenreSerializer(obj)
        return serializer.data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = CategorySerializer(obj)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True)
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        title = Title.objects.get(id=obj.id)
        score = title.reviews.all().aggregate(Avg('score'))
        return score['score__avg']

    def validate(self, data):
        if not data.get('year'):
            return data
        if data.get('year') > datetime.now().year:
            raise ValidationError(
                'Год выпуска произведения не может быть в будущем.')
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        title_genre_objs = [
            TitleGenre(title=title, genre=genre) for genre in genres]
        TitleGenre.objects.bulk_create(title_genre_objs)
        return title


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data['username']
        prog = re.compile(r'^[\w.@+-]+\Z', re.ASCII)
        result = prog.match(username)
        if not result:
            raise ValidationError(
                'Введи корректное имя пользователя. Можно использовать '
                'только латинские буквы, цифры и символы "@/./+/-/_" .')
        if username == 'me':
            raise ValidationError(
                'Придумай другое имя пользователя, это уже занято.')
        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        to_email = validated_data.get('email')
        user = User.objects.create(username=username, email=to_email)
        code = default_token_generator.make_token(user)
        msg = ('Привет! Воспользуйся, пожалуйста, '
               f'этим кодом для получения токена {code}')
        send_mail(
            subject='Код-подтверждение',
            message=msg,
            recipient_list=[to_email],
            from_email=None,
            fail_silently=False
        )
        user.confirmation_code = code
        return user

    def update(self, instance, validated_data):
        to_email = validated_data.get('email')
        if instance.email != to_email:
            raise serializers.ValidationError(
                'Введен неверный адрес электронной почты.')
        code = default_token_generator.make_token(instance)
        msg = ('Привет! Воспользуйся, пожалуйста, '
               f'этим кодом для получения токена {code}')
        send_mail(
            subject='Код-подтверждение',
            message=msg,
            recipient_list=[to_email],
            from_email=None,
            fail_silently=False
        )
        instance.confirmation_code = code
        instance.save()
        return instance


class AdminUserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        username = data.get('username')
        if not username:
            return data
        prog = re.compile(r'^[\w.@+-]+\Z', re.ASCII)
        result = prog.match(username)
        if not result:
            raise ValidationError(
                'Введи корректное имя пользователя. Можно использовать '
                'только латинские буквы, цифры и символы "@/./+/-/_" .')
        if username == 'me':
            raise ValidationError(
                'Придумай другое имя пользователя, это уже занято.')
        return data

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    def validate(self, data):
        username = data.get('username')
        if not username:
            return data
        prog = re.compile(r'^[\w.@+-]+\Z', re.ASCII)
        result = prog.match(username)
        if not result:
            raise ValidationError(
                'Введи корректное имя пользователя. Можно использовать '
                'только латинские буквы, цифры и символы "@/./+/-/_" .')
        if username == 'me':
            raise ValidationError(
                'Придумай другое имя пользователя, это уже занято.')
        return data

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True,
                              slug_field='username',
                              default=serializers.CurrentUserDefault())
    title = HiddenField(default=None)

    def get_title(self, obj):
        return self.context['title']

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        super().validate(data)
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id'])
            if Review.objects.filter(author=user, title__id=title_id).exists():
                raise serializers.ValidationError(
                    'Duplicated review')
            return data
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username',
                              default=serializers.CurrentUserDefault())
    review = PrimaryKeyRelatedField(read_only=True)
    title = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
