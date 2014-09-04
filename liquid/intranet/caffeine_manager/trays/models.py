from django.db import models
from django.core.validators import MinValueValidator
from intranet.caffeine_manager.soda.models import Soda

class Tray(models.Model):
    tray_number=models.IntegerField(max_length=11, validators=[MinValueValidator(1)], unique=True)
    soda=models.ForeignKey(Soda, blank=True, null=True, on_delete=models.SET_NULL)
    quantity=models.IntegerField(max_length=11, default=0, validators=[MinValueValidator(0)])
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.5)
    enabled=models.BooleanField(default=False)
    detect_override=models.BooleanField(default=False)
