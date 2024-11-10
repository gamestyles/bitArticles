import uuid


def retrieve_fingerprint(fingerprint: str):
    """
    Checks the validity of given fingerprint and returns the uuid instance of it.

    We assume the fingerprints are all UUIDv4!
    """
    try:
        uuid_obj = uuid.UUID(fingerprint, version=4)
    except ValueError:
        return None

    return uuid_obj
