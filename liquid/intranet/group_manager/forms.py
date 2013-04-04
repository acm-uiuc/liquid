from django.forms import ModelForm, ModelChoiceField
from django.forms.models import inlineformset_factory
from intranet.models import Group, GroupMember
from utils.widgets import SelectTimeWidget,BootstrapDateInput
from utils.django_mailman.models import List

GroupMemberFormSet = inlineformset_factory(Group, GroupMember,fields=('is_admin','is_chair','status'),can_delete=False,extra=0)

class GroupForm(ModelForm):
  mailing_list = ModelChoiceField(queryset=List.objects.order_by('name'))
  class Meta:
    model = Group
    exclude = ['members']
    widgets = {'meeting_time': SelectTimeWidget,'date_formed':BootstrapDateInput}

