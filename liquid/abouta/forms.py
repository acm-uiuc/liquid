from django.forms import ModelForm
from intranet.models import Job

class JobForm(ModelForm):
  class Meta:
      model = Job
      exclude = ['approved','sent']