from django.forms import ModelForm
from django import forms
from intranet.event_manager.models import Event

class EventForm(ModelForm):
  class Meta:
    model = Event
    widgets = {'sponsors': forms.CheckboxSelectMultiple}

