import pytest
import uuid

from django.urls import reverse


def test_unauthorized_api_request(api_client):
    """
    Tests an api with wrong type of fingerprint.
    """
    url = reverse('api-articles')
    not_a_valid_fingerprint_id = "not_a_valid_fp_id"
    response = api_client.get(url, headers={'X-FINGERPRINT-ID': not_a_valid_fingerprint_id})
    assert response.status_code == 401


def test_forbidden_api_request(api_client):
    """
    Tests an api without fingerprint id.
    """
    url = reverse('api-articles')
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_api_request(api_client):
    """
    Tests an api with correct fingerprint id.
    """
    url = reverse('api-articles')
    fp_id = uuid.uuid4()
    response = api_client.get(url, headers={'X-FINGERPRINT-ID': str(fp_id)})
    assert response.status_code == 200
