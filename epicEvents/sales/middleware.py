from django.http import HttpResponseBadRequest


class DeleteSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'DELETE' and not request.path.endswith('/'):
            return HttpResponseBadRequest('A DELETE request must end with a slash (/) after the resource URI."')
        response = self.get_response(request)
        return response
