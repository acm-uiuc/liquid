from django.forms import ModelForm
from intranet.caffeine_manager.models import Soda, Tray
from intranet.models import Vending

class SodaForm(ModelForm):
   class Meta:
      model = Soda

class TrayForm(ModelForm):
   class Meta:
      model = Tray
      
class VendingForm(ModelForm):
   class Meta:
      model = Vending
      fields = ['balance']
