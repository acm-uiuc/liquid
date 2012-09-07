from django.forms import ModelForm
from intranet.models import Resume
from django.forms.models import modelformset_factory

ResumeFormSet = modelformset_factory(Resume,fields = ['approved'],can_delete=True,extra=0)