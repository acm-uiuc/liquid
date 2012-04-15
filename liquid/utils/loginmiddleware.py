from django.conf import settings
from django.http import HttpResponseRedirect

import re

class RequireLoginMiddleware(object):
    def __init__(self):
        self.urls = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/login')
    
    def process_request(self, request):
        for url in self.urls:
            if url.match(request.path) and request.user.is_anonymous():
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
