from django.forms import ModelForm
from intranet.caffeine_manager.soda.models import Soda

class SodaForm(ModelForm):
    class Meta:
        model=Soda
