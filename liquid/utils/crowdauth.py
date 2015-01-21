import crowd
import settings
from intranet.models import Member

class CrowdAuthenticationBackend:
   supports_object_permissions = False
   supports_anonymous_user = False
   supports_inactive_user = False
   def _client(self):
      return crowd.CrowdServer(
         settings.CROWD_API_URL,
         settings.CROWD_APP_NAME,
         settings.CROWD_APP_PASSWORD,
         ssl_verify=True
      )

   def authenticate(self,username=None, password=None):
      c = self._client()
      # success is actually a dict of attributes if valid
      # in the future maybe we will sync those to liquid
      success = c.auth_user(username, password)
      if success:
         return self.get_user_by_username(username)
      else:
         return None

   # Use this if you have the username (netid)
   def get_user_by_username(self, username):
      try:
         return Member.objects.get(username=username)
      except Member.DoesNotExist:
         return None

   # This is if we have the underlying user pk
   def get_user(self, user_id):
      try:
         return Member.objects.get(pk=user_id)
      except Member.DoesNotExist:
         return None
