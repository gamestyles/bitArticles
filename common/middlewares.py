import logging

from django.utils.deprecation import MiddlewareMixin

from common.fingerprint import retrieve_fingerprint
from .utils import HttpResponseUnauthorized


_logger = logging.getLogger('common.middleware')


class UserFingerprintMiddleware(MiddlewareMixin):
    """
    This middleware checks Authorization request header for user identification.

    Because we don't have profile and authentication for the user, we assume the client sends the fingerprint of
    the user to us to identify him.

    If the fingerprint is not given we don't interfere the process of the request. (e.x admin panel)
    """
    def process_request(self, request):
        fingerprint_header = request.headers.get('X-FINGERPRINT-ID')
        _logger.info(f"here: {fingerprint_header}")

        if fingerprint_header:
            fp = retrieve_fingerprint(fingerprint_header)
            _logger.info("here fp")
            if fp:
                request.user_fingerprint = fp
                _logger.info("here")
            else:
                return HttpResponseUnauthorized()
