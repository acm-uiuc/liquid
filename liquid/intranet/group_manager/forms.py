from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from intranet.models import Group, GroupMember
from utils.widgets import SelectTimeWidget,BootstrapDateInput

GroupMemberFormSet = inlineformset_factory(Group, GroupMember,fields=('is_admin','is_chair','status'),can_delete=False,extra=0)

class GroupForm(ModelForm):
  class Meta:
    model = Group
    exclude = ['members']
    widgets = {'meeting_time': SelectTimeWidget,'meeting_date':BootstrapDateInput}

