# from django.core.exceptions import PermissionDenied
# from functools import wraps

# def role_required(allowed_roles=[]):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             if request.user.role not in allowed_roles:
#                 raise PermissionDenied  # 403 Forbidden
#             return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator
from django.http import HttpResponseForbidden

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper
    return decorator

