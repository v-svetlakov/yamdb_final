from rest_framework import serializers

from reviews.models import Comment, Review
from titles.serializers import TitleGeneralSerializer


class ReviewSerializer(serializers.ModelSerializer):
    title = TitleGeneralSerializer(many=False, read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Review
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    review = ReviewSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date', 'review']
