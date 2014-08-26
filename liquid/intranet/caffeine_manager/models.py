from django.db import models
from intranet.models import Member
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
from django.core.validators import MinValueValidator

class Soda(models.Model):
   name = models.CharField(max_length=32)
   calories = models.IntegerField(max_length=11, default=0)
   caffeine = models.IntegerField(max_length=11, default=0)
   cost = models.DecimalField(default=0.5, decimal_places = 2, max_digits = 6)
   total_sold = models.IntegerField(max_length=11, default=0)

   def __unicode__(self):
      return unicode(self.name)

class Tray(models.Model):
   tray_number = models.IntegerField(max_length = 11, validators = [MinValueValidator(1)], unique = True)
   soda = models.ForeignKey(Soda, blank=True, null=True, on_delete=models.SET_NULL)
   quantity = models.IntegerField(max_length = 11, default = 0)
   price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.5)
   enabled = models.BooleanField(default = False)
   detect_override = models.BooleanField(default = False)
