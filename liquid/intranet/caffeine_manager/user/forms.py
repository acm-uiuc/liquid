from django.forms import ModelForm
from intranet.models import Vending

class VendingForm(ModelForm):
    class Meta:
        model=Vending
        fields=['balance']
