from django.forms import ModelForm,ValidationError
from intranet.member_manager.models import Member

class NewMemberForm(ModelForm):
  class Meta:
    model = Member
    fields = ('uin', 'netid')

class EditMemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ('first_name','last_name','joined','left_uiuc','status')