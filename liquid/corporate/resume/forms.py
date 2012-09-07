from django.forms import ModelForm
from intranet.models import ResumePerson, Resume

class ResumePersonForm(ModelForm):
  class Meta:
      model = ResumePerson

class ResumeForm(ModelForm):
  class Meta:
      model = Resume
      exclude = ['approved','person']