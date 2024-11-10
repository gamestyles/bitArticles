from django.http import HttpResponse


class HttpResponseUnauthorized(HttpResponse):
    def __init__(self):
        super().__init__('401 Unauthorized', status=401)
