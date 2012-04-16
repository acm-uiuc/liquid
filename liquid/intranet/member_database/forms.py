from django.forms import ModelForm,ValidationError
from intranet.models import Member

class NewMemberForm(ModelForm):
  class Meta:
    model = Member
    fields = ('uin', 'username')

class EditMemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ('first_name','last_name','uin','status')
