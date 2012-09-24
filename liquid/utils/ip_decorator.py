from functools import wraps

from django.core.exceptions import PermissionDenied

def ips_required(ips=[]):    
   def decorator(func):
      def inner_decorator(request,*args, **kwargs):
         if request.META['REMOTE_ADDR'] in ips:
            return func(request, *args, **kwargs)
         else:
            raise PermissionDenied
            return False
      return wraps(func)(inner_decorator)
   return decorator


def password_get(password):    
   def decorator(func):
      def inner_decorator(request,*args, **kwargs):
         if request.GET.get('password') == password:
            return func(request, *args, **kwargs)
         else:
            raise PermissionDenied
            return False
      return wraps(func)(inner_decorator)
   return decorator
   