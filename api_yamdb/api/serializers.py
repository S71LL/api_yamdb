import re
from datetime import datetime

from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework.relations import SlugRelatedField

from users.models import User
from titles.models import Review, Comment, Title, Category, Genre, TitleGenre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GenreField(serializers.Field):
    def to_internal_value(self, data):
        lst = []
        for genre_slug in data:
            genre = get_object_or_404(Genre, slug=genre_slug)
            serializer = GenreSerializer(data=genre)
            if serializer.is_valid():
                lst.append(serializer.data)
        return lst

    def to_representation(self, value):
        return super().to_representation(value)


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        return Review.objects.filter(title_id=obj.id).aggregate(Avg('score'))

    def validate(self, data):
        if not isinstance(data.get('year'), int):
            raise ValidationError('Поле "year" должно юыть целым числом.')
        if data.get('year') > datetime.now().year:
            raise ValidationError(
                'Год выпуска произведения не может быть в будущем.')
        return data


"""
    def create(self, validated_data):
        genres = validated_data.pop('genre')
        print(genres)
        title = Title.objects.create(**validated_data)
        for genre_slug in genres:
            genre = get_object_or_404(Genre, slug=genre_slug)
            TitleGenre.objects.create(title=title, genre=genre)
        return title
"""

class SignupSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = User
        fields = ('username', 'email')


class UserTokenSerializer(serializers.ModelSerializer):
    token = serializers.SlugRelatedField(
        slug_field='key',
        read_only=True
    )

    class Meta:
        model = User
        fields = ('token',)


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
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'title')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
