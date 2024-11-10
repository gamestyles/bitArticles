from rest_framework.permissions import BasePermission


class IsFingerprintAvailable(BasePermission):
    """
    Checks the availability of user_fingerprint attribute for the request

    We permit requests that have fingerprint to access APIs.
    """
    def has_permission(self, request, view):
        try:
            return bool(request.user_fingerprint)
        except AttributeError:
            return False
