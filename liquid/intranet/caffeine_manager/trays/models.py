from django.db import models
from django.core.validators import MinValueValidator
from intranet.caffeine_manager.soda.models import Soda

# Add in_db attrib to valid Meta options
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

from django.db import models

# === Hack to support Caffeine's "enum(t,f)" boolean fields ===
# From http://gdorn.circuitlocution.com/blog/2010/11/29/legacy-booleanfield-in-django.html
class tfBooleanField(models.BooleanField):
    __metaclass__ = models.SubfieldBase #need this for django to know to call to_python()

    def __init__(self, *args, **kwargs):
        super(tfBooleanField, self).__init__(*args, **kwargs)

    """
    Disabled (using 'return None') because:
    1) This is only used during migrations to CREATE TABLEs
    2) "enum('t', 'f')" causes a syntax error in Docker
    3) The relevant tables already exist anyway
    Docs: https://docs.djangoproject.com/en/1.6/howto/custom-model-fields/
    """
    def db_type(self, connection):
        return None

    def to_python(self, value):
        if value in (True, False):
            return bool(value)
        if value in ('t', 'f'):
            return value == 't'
        return False

    def get_prep_value(self, value):
        if value in ('t', 'f'):
            return value
        if value:
            return 't'
        return 'f'

    def get_prep_lookup(self, lookup_type, value):
        if value in ('1','0'): #special case for dealing with admin, see BooleanField.get_prep_lookup
            value = bool(value)
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)
# === End hack ===

class Tray(models.Model):
    id=models.IntegerField(max_length=11, validators=[MinValueValidator(1)], unique=True, primary_key=True, verbose_name='Tray ID', db_column='tid')
    soda=models.ForeignKey(Soda, blank=True, null=True, on_delete=models.SET_NULL, db_column='sid')
    qty=models.IntegerField(max_length=11, default=0, validators=[MinValueValidator(0)], verbose_name='Quantity')
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.5)
    enabled=tfBooleanField(default='f')
    sense_override=tfBooleanField(default='f', verbose_name='Detect override')

    class Meta:
        in_db='soda'
        db_table='trays'
