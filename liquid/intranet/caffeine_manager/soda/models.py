from django.db import models
from django.core.validators import MinValueValidator
from intranet.models import Member

class Soda(models.Model):
    name = models.CharField(max_length=32)
    calories = models.IntegerField(max_length=11, default=0, validators = [MinValueValidator(0)])
    caffeine = models.IntegerField(max_length=11, default=0, validators = [MinValueValidator(0)])
    cost = models.DecimalField(default=0.5, decimal_places = 2, max_digits = 6)
    total_sold = models.IntegerField(max_length=11, default=0, validators = [MinValueValidator(0)])
    votes = models.ManyToManyField(Member)

    def __unicode__(self):
        return unicode(self.name)
