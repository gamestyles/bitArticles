import pytest
from bitArticles import settings
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient


# import fixtures here
pytest_plugins = [
    'pytest_asyncio'
]

fixtures = [

]

pytest_plugins += fixtures


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def requests_client():
    return RequestsClient()
