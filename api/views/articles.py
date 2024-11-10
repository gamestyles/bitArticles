from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.articles import ArticleSerializer, ArticleScoreUserSerializer, ArticleScoreSerializer
from article.handlers import ArticleScoreUserHandler
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
    def get_serializer(self, *args, **kwargs):
        return ArticleScoreUserSerializer(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: ArticleScoreSerializer
        }
    )
    def put(self, request, article_id: int, *args, **kwargs):
        """Creates a new score for the specified article, if exists, updates it."""
        # serialize data and validation
        serialized_data = self.get_serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        # handle the request with given data
        as_handler = ArticleScoreUserHandler(serialized_data.validated_data, request.user_fingerprint, article_id)
        data = as_handler.handle_put()

        return Response(data=data, status=status.HTTP_200_OK)
