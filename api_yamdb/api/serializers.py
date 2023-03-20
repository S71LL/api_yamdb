import re

from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from users.models import User
from titles.models import Review, Comment, Title, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


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
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
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
