from functools import wraps

from intranet.models import Group
from django.core.exceptions import PermissionDenied

def group_admin_required(groups=[]):    
   def decorator(func):
      def inner_decorator(request,*args, **kwargs):
         user_groups = request.user.groupmember_set.filter(is_admin__exact=True).filter(group__name__in=groups)
         if not user_groups:
            raise PermissionDenied()
         else:
            return func(request, *args, **kwargs)
      return wraps(func)(inner_decorator)
   return decorator