import ldap
import settings
from intranet.models import Member


class ActiveDirectoryGroupMembershipSSLBackend:
   supports_object_permissions = False
   supports_anonymous_user = False
   supports_inactive_user = False
   def authenticate(self,username=None,password=None):
      try:
         if len(password) == 0:
            return None
         l = ldap.initialize(settings.AD_LDAP_URL)
         binddn = settings.AD_BIND_DN.format(username)
         l.simple_bind_s(binddn,password)
         l.unbind_s()
         return self.get_or_create_user(username,password)

      except ImportError:
         pass
      except ldap.INVALID_CREDENTIALS:
         pass

   def get_or_create_user(self, username, password):
      try:
         user = Member.objects.get(username=username)
      except Member.DoesNotExist:
         return None

      return user

   def get_user(self, user_id):
      try:
         return Member.objects.get(pk=user_id)
      except Member.DoesNotExist:
         return None
