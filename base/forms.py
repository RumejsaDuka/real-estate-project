from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=False)
    interest = forms.ChoiceField(
        choices=[
            ('', 'Zgjidh një opsion'),
            ('buying', 'Buying a Property'),
            ('selling', 'Selling a Property'),
            ('renting', 'Renting / Leasing'),
            ('investment', 'Investment Advice'),
            ('valuation', 'Property Valuation'),
            ('general', 'General Inquiry'),
        ],
        required=False
    )
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    privacy = forms.BooleanField(required=True)
