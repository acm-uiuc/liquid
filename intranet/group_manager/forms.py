from django.forms import ModelForm
from intranet.group_manager.models import Group

class GroupForm(ModelForm):
  class Meta:
      model = Group
