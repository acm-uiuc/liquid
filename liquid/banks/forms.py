from django.forms import ModelForm, CheckboxSelectMultiple, HiddenInput
from utils.widgets import SplitSelectDateTimeWidget
from banks.models import BanksPost
from pagedown.widgets import AdminPagedownWidget, PagedownWidget

class PostForm(ModelForm):

  class Meta:
    model = BanksPost
    widgets = {
      'content_markdown' : AdminPagedownWidget(),
    }
    exclude = ['creator','content_markup', 'slug']
