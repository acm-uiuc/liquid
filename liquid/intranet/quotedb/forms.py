from django.forms import ModelForm
from quotedb.models import Quote

class QuoteForm(ModelForm):
   class Meta:
      model = Quote
      fields = ['quote_text', 'quote_source']
