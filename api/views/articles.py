from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.serializers.articles import ArticleSerializer
from article.models import Article


class ArticleAPIView(ListModelMixin, GenericAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
