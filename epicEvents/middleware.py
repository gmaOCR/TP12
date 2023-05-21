from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_authenticated:
            return redirect('/admin/')
        elif request.path.startswith('/admin/') and not request.user.is_superuser:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>')
        elif request.path.startswith('/admin/') and request.user.role != 'gestion':
            return HttpResponseForbidden('<h1>403 Forbidden</h1>')

        response = self.get_response(request)
        return response

class NotFoundMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return HttpResponseNotFound('<h1>Page not found.</h1>')
        return response
