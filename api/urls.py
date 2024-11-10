import os

from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions

from api.views import articles
from django.conf import settings

endpoints = [
    # article endpoints
    path('articles/', articles.ArticleAPIView.as_view(), name='api-articles'),
    # path('articles/<int:id>/score/', articles.ArticleScoreAPIView.as_view(), name='api-articles-details-score'),
]


class PublicAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = os.path.join("/", settings.API_PREFIX)
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="BitArticles API",
        default_version=settings.API_VERSION,
    ),
    public=True,
    patterns=endpoints,
    generator_class=PublicAPISchemeGenerator,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-docs'),
]

urlpatterns += endpoints
