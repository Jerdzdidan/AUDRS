from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []
        
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if request.user.role not in allowed_roles:
                messages.warning(request, "Unauthorized access")
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator