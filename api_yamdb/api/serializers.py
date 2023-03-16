from rest_framework import serializers

from titles.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'title')
        model = Review
