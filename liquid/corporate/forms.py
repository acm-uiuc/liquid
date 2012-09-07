from django.forms import ModelForm
from intranet.models import Job, ResumePerson, Resume

class JobForm(ModelForm):
  class Meta:
      model = Job
      exclude = ['status','sent']

class ResumePersonForm(ModelForm):
  class Meta:
      model = ResumePerson

class ResumeForm(ModelForm):
  class Meta:
      model = Resume
      exclude = ['approved','person']