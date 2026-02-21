from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden

error_403_html = """
<html>
    <head>
        <title>403 Forbidden</title>
    </head>

    <body>
        <h3>403 - Access Forbidden</h3>
        <p>You are not authorized to access this page.</p>
        <a href="/">Return to home</a>
    </body>
</html>
"""

def login_and_role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required

        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if required_role == 'customer' and not user.is_customer:
                return HttpResponseForbidden(error_403_html)
            
            if required_role == 'seller' and not user.is_seller:
                return HttpResponseForbidden(error_403_html)
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view

    return decorator