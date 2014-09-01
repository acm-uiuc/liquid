from django.forms import ModelForm
from intranet.caffeine_manager.trays.models import Tray

class TrayForm(ModelForm):
   class Meta:
      model = Tray
