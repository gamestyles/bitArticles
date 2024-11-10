from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView

from api.serializers.articles import ArticleSerializer
from article.models import Article, ArticleScore


class ArticleAPIView(ListModelMixin, GenericAPIView):
    """
    Article Resource\n

    Retrieve paginated list of articles and user related score
    """
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        # Paginate the queryset to get only the articles on the current page
        page = self.paginate_queryset(self.get_queryset())

        # Retrieve scores only for articles in the current page
        article_ids = [article.id for article in page]
        scores = ArticleScore.objects.filter(
            article_id__in=article_ids,
            user_id=request.user_fingerprint,
            is_suspicious=False
        )
        user_scores = {score.article_id: score.score for score in scores}

        # Pass the scores to the serializer context
        serializer = self.get_serializer(page, many=True, context={'user_scores': user_scores})
        return self.get_paginated_response(serializer.data)


class ArticleScoreAPIView(APIView):
    """
    Article user scores\n

    Rate an article for specific user
    """

    def put(self, request, *args, **kwargs):
        pass
