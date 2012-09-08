from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

import re

class RequireLoginMiddleware(object):
    def __init__(self):
        self.urls_member = tuple([re.compile(url) for url in settings.LOGIN_MEMBER_REQUIRED_URLS])
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/login')
    
    def process_request(self, request):
        print request.user.__class__.__name__
        for url in self.urls_member:
            if url.match(request.path) and request.user.is_anonymous():
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
            if url.match(request.path) and request.user.__class__.__name__ != "Member":
               raise PermissionDenied()

