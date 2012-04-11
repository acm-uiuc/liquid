import ldap
import settings
from intranet.member_manager.models import Member


class ActiveDirectoryGroupMembershipSSLBackend:
  supports_object_permissions = False
  supports_anonymous_user = False
  supports_inactive_user = False
  def authenticate(self,username=None,password=None):
      try:
         if len(password) == 0:
            return None
         l = ldap.initialize(settings.AD_LDAP_URL)
         binddn = "uid=%s,ou=People,dc=acm,dc=uiuc,dc=edu" % (username)
         l.simple_bind_s(binddn,password)
         l.unbind_s()
         return self.get_or_create_user(username,password)

      except ImportError:
         pass
      except ldap.INVALID_CREDENTIALS:
         pass

  def get_or_create_user(self, username, password):
      try:
         user = self.user_class.objects.get(netid=username)
      except self.user_class.DoesNotExist:
         return None

      return user

   def get_user(self, user_id):
      try:
         return self.user_class.objects.get(pk=user_id)
      except self.user_class.DoesNotExist:
         return None

   @property
   def user_class(self):
      if not hasattr(self, '_user_class'):
         self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
      if not self._user_class:
         raise ImproperlyConfigured('Could not get custom user model')
      return self._user_class
