from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# Create your decorators here.

def is_staff_or_admin(user):
    return user.is_staff or user.is_admin


def admin_required(view_func):
    # Signed-out users go to the login page, signed-in non-admins get a 403.
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


def staff_required(view_func):
    # Lets in staff (professors) and admins.
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_staff_or_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)
