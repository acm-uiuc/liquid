from django.forms import ModelForm
from intranet.models import ResumePerson, Resume

class ResumePersonForm(ModelForm):
  class Meta:
      model = ResumePerson
      exclude = ['ldap_name']

class ResumeForm(ModelForm):
  class Meta:
      model = Resume
      exclude = ['approved','person']