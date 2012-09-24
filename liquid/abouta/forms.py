from django.forms import ModelForm
from intranet.models import Job, PreMember

class PreMemberForm(ModelForm):
   class Meta:
      model = PreMember
      exclude = ['created_at']