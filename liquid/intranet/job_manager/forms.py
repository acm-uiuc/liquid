from django.forms import ModelForm
from intranet.models import Job
from django.forms.models import modelformset_factory

JobFormSet = modelformset_factory(Job,fields = ['status'],can_delete=False,extra=0)