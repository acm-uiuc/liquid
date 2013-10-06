from django.forms import ModelForm
from intranet.quote.models import Quote

class QuoteForm(ModelForm):
   class Meta:
      model = Quote
      fields = ['quote_text', 'quote_sources', 'quote_posters']
