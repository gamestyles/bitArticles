import pytest
from django.urls import reverse
from rest_framework import status

from article.models import Article, ArticleScore


@pytest.mark.django_db
def test_score_specific_article(
        api_client,
        create_fingerprint_id_header,
):
    """
    Tests happy path of creating a score for an article

    Requesting again to score that article results to update the score.
    """
    # create article
    article = Article.objects.create(title=f"Article")

    # url with given article_id
    url = reverse("api-articles-details-score", args=[article.id])

    # Get fp header
    headers = create_fingerprint_id_header

    # given payload
    data = {
        "score": 5
    }

    # Send request to the endpoint
    response = api_client.put(url, data=data, format='json', headers=headers)

    # Check status code
    assert response.status_code == status.HTTP_200_OK

    assert ArticleScore.objects.count() == 1

    assert response.data['article_id'] == article.id
    assert response.data['user_id'] == headers.get('X-FINGERPRINT-ID')
    assert response.data['score'] == data.get('score')
    assert 'created_at' in response.data

    second_data = {
        "score": 2
    }

    second_response = api_client.put(url, data=second_data, format='json', headers=headers)

    assert second_response.status_code == status.HTTP_200_OK

    # still one score exists
    assert ArticleScore.objects.count() == 1

    assert second_response.data['article_id'] == article.id
    assert second_response.data['user_id'] == headers.get('X-FINGERPRINT-ID')
    assert second_response.data['score'] == second_data.get('score') == ArticleScore.objects.first().score
    assert 'created_at' in second_response.data
