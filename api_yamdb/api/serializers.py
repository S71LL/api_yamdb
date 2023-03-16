from rest_framework import serializers

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        # read_only_fields = ('name', 'slug')
