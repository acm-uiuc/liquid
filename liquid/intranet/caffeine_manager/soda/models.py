from django.db import models
from django.core.validators import MinValueValidator

# Add in_db attrib to valid Meta options
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

class Soda(models.Model):
    id = models.AutoField(primary_key=True, db_column='sid')
    name=models.CharField(max_length=64)
    calories=models.IntegerField(max_length=11, default=0, validators=[MinValueValidator(0)])
    caffeine=models.FloatField(default=0, validators=[MinValueValidator(0)])
    cost=models.DecimalField(default=0.5, decimal_places=2, max_digits=10)
    dispensed=models.IntegerField(max_length=11, default=0, validators=[MinValueValidator(0)])
    base_price=models.DecimalField(default=0.5, decimal_places=2, max_digits=10)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        in_db='soda'
        db_table='sodas'
