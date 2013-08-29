from django.forms import ModelForm, CheckboxSelectMultiple, HiddenInput
from utils.widgets import SplitSelectDateTimeWidget
from banks.models import BanksPost, Comment

class PostForm(ModelForm):
  class Meta:
    model = BanksPost
    exclude = ['creator']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    exclude ="post"
