from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'interest', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_subject(self):
        return self.cleaned_data['subject'].strip()

    def clean_message(self):
        return self.cleaned_data['message'].strip()
