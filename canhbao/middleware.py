from django.http import HttpResponseForbidden
from django.urls import resolve

def has_permission(user, url):
    
    view_func = resolve(url).func

    if hasattr(view_func, 'permission_required'):
      
        permission = view_func.permission_required
        if not user.has_perm(permission):
            return False

 
    return True

class CustomAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
      
        if not has_permission(request.user, request.path):
            return HttpResponseForbidden('You do not have permission to access this page')
        
        response = self.get_response(request)
        return response
