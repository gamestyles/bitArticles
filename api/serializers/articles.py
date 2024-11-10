from rest_framework import serializers
from article.models import Article

from django.utils.translation import gettext_lazy as _


class ArticleSerializer(serializers.ModelSerializer):
    """
    Article serializer that serializes all fields from Article model

    with additional user score, if user has scored for the article
    """
    user_score = serializers.SerializerMethodField(help_text=_("the score that user gave to the article"))

    class Meta:
        model = Article
        fields = "__all__"

    def get_user_score(self, obj):
        # Retrieve user score from the context dictionary
        user_scores = self.context.get('user_scores', {})
        return user_scores.get(obj.id)


class ArticleScoreUserSerializer(serializers.Serializer):
    """User Score data for rating an Article"""
    score = serializers.ChoiceField(choices=range(1, 6), help_text=_("the score to give to specified article"))


class ArticleScoreSerializer(serializers.Serializer):
    """Serializes a response for scoring an article"""
    article_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.UUIDField(help_text="the user id who scored")
    score = serializers.IntegerField(
        help_text="the score that can be between 1 to 5"
    )
    created_at = serializers.DateTimeField(read_only=True)
