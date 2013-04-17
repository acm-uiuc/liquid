from django.forms import ModelForm
from conference.models import Company

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["company_name", "first_name", "last_name", "email", "type"]
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        classes = {
            'company_name': 'span4',
            }
        labels = {
            'company_name' : 'Company Name',
            'first_name' : 'Contact First Name',
            'last_name' : 'Contact Last Name',
            'email' : 'Contact Email',
            }
        for field, label in labels.items():
            self.fields[field].label = label
        for field, css in classes.items():
            if field in self.fields:
                self.fields[field].widget.attrs['class'] = css
