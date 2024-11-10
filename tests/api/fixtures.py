import uuid
import pytest


@pytest.fixture
def create_fingerprint_id_header():
    headers = {
        "X-FINGERPRINT-ID": str(uuid.uuid4())
    }
    return headers
