from rest_framework import serializers
from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Article serializer that serializes all fields from Article model

    with additional user score, if user has scored for the article
    """
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = "__all__"

    def get_user_score(self, obj):
        # Retrieve user score from the context dictionary
        user_scores = self.context.get('user_scores', {})
        return user_scores.get(obj.id)
