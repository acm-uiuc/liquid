from django.forms import ModelForm, CheckboxSelectMultiple, HiddenInput
from utils.widgets import SplitSelectDateTimeWidget
from intranet.models import Event

class EventForm(ModelForm):
  class Meta:
    model = Event
    widgets = {'sponsors': CheckboxSelectMultiple,'starttime': SplitSelectDateTimeWidget,'endtime': SplitSelectDateTimeWidget}
    exclude = ['creator']
