from django import forms

class InviteForm(forms.Form):
    from_email = forms.EmailField(label="From")
    to_email = forms.EmailField(label="To")
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        classes = {
            'subject': 'span9',
            'body': 'span9',
            }

        for field, css in classes.items():
            if field in self.fields:
                self.fields[field].widget.attrs['class'] = css
