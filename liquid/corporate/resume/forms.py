from django.forms import ModelForm, EmailField
from intranet.models import ResumePerson, Resume
from django.contrib.auth.models import User

class ResumePersonForm(ModelForm):
  class Meta:
      model = ResumePerson
      exclude = ['ldap_name']

class ResumeForm(ModelForm):
  class Meta:
      model = Resume
      exclude = ['approved','person']

class EmailChangeForm(ModelForm):
  email = EmailField(required=True)
  class Meta:
      model = User
      fields = ['email']
        