from django.forms import ModelForm
from django import forms
from intranet.models import Event

class EventForm(ModelForm):
  class Meta:
    model = Event
    widgets = {'sponsors': forms.CheckboxSelectMultiple}

