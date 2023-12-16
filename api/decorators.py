from functools import wraps
from django.utils import timezone


def update_last_request(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_request = timezone.now()
            request.user.save()

        return view_func(request, *args, **kwargs)
    return wrapped_view
