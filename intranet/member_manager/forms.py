from django.forms import ModelForm
from intranet.member_manager.models import Member

class MemberForm(ModelForm):
  class Meta:
      model = Member
