from rest_framework import serializers
from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer that serializes all fields from Article model"""
    class Meta:
        model = Article
        fields = "__all__"
