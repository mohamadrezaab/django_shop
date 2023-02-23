from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from .views import UserRegisterVerifyCodeView, UserLogoutView, UserLoginView
from django.shortcuts import redirect

class UserActionMiddleware(MiddlewareMixin):
    ACTIONS = {
        'login': 'User logged in',
        'logout': 'User logged out',
        'register': 'User registered',
    }

    def process_view(self, request, view_func, view_args, view_kwargs):
        # check if the view is a user action (login, logout, or register)
        if hasattr(view_func, 'view_class'):
            if view_func.view_class == UserLoginView:
                action = 'login'
            elif view_func.view_class == UserLogoutView:
                action = 'logout'
            elif view_func.view_class == UserRegisterVerifyCodeView:
                action = 'register'
            else:
                return None

            # log the user action
            log_data = {
                'user_id': request.user.id if request.user.is_authenticated else None,
                'action': self.ACTIONS[action],
                'timestamp': datetime.now(),
                'request_method': request.method,
                'request_path': request.path,
                'request_body': request.body.decode('utf-8'),
            }
            # save log_data to the database or log it to a file or send it to a remote logging service
            print(log_data)
        return None
class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != '/login/':
            return redirect('/login/')
        response = self.get_response(request)
        return response

