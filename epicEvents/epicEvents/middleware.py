from django.http import HttpResponseForbidden
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
