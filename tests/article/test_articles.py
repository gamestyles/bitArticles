import pytest
from django.urls import reverse
from rest_framework import status

from article.models import Article


@pytest.mark.django_db
def test_article_api_view_pagination(
        api_client,
        create_fingerprint_id_header,
        settings
):
    url = reverse("api-articles")

    # Create multiple articles to test pagination
    for i in range(15):
        Article.objects.create(title=f"Article {i+1}")

    # Get fp header
    headers = create_fingerprint_id_header

    # Send request to the endpoint
    response = api_client.get(url, headers=headers)

    # Check status code
    assert response.status_code == status.HTTP_200_OK

    # Check pagination structure
    assert "results" in response.data
    assert "count" in response.data
    assert "next" in response.data
    assert "previous" in response.data

    # Check number of articles per page
    assert len(response.data["results"]) <= settings.REST_FRAMEWORK["PAGE_SIZE"]
    assert response.data["count"] == 15

    # Check fields in serialized data
    for article in response.data["results"]:
        assert "id" in article
        assert "title" in article
        assert "created_at" in article
