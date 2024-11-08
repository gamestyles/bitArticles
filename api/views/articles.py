from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ArticleAPIView(APIView):
    # def get_serializer(self, *args, **kwargs):
    #     return ArticleSerializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Get Articles list\n
        """
        # TODO: just a test
        return Response(data="Hello", status=status.HTTP_200_OK)
