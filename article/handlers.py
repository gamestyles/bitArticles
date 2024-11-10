from .models import ArticleScore
from api.serializers.articles import ArticleScoreSerializer


class ArticleScoreUserHandler:

    def __init__(self, data: str, user_id: str, article_id: int):
        self.data = data
        self.user_id = user_id
        self.article_id = article_id

    def handle_put(self):
        """
        Handling when user wants to score an article

        It will update the score if exists.
        If the user score has been flagged as suspicious, then a new score will be created.
        """
        try:
            as_obj = ArticleScore.objects.get(article_id=self.article_id, user_id=self.user_id, is_suspicious=False)
            as_obj.score = self.data.get("score")
            as_obj.save(update_fields=["score", "modified_at"])
        except ArticleScore.DoesNotExist:
            as_obj = ArticleScore.objects.create(
                article_id=self.article_id,
                user_id=self.user_id,
                score=self.data.get("score")
            )

        serializer = ArticleScoreSerializer(as_obj)

        return serializer.data
