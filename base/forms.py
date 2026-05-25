from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ContactMessage, Message, Property, PropertyImage


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Emri i perdoruesit',
        }
        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Fjalekalimi'
        self.fields['password2'].label = 'Konfirmo fjalekalimin'
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].error_messages['required'] = 'Shkruani emrin e perdoruesit.'
        self.fields['email'].error_messages['required'] = 'Shkruani email-in.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Emri i perdoruesit')
    password = forms.CharField(label='Fjalekalimi', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Te dhenat e hyrjes nuk jane te sakta.',
        'inactive': 'Kjo llogari nuk eshte aktive.',
    }


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'price',
            'location',
            'image',
            'listing_type',
            'beds',
            'baths',
            'sqft',
        ]
        labels = {
            'title': 'Titulli',
            'description': 'Pershkrimi',
            'price': 'Cmimi',
            'location': 'Vendndodhja',
            'image': 'Foto kryesore',
            'listing_type': 'Lloji i listes',
            'beds': 'Dhoma gjumi',
            'baths': 'Banjo',
            'sqft': 'Siperfaqja',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        labels = {
            'image': 'Foto shtese',
            'caption': 'Pershkrim i fotos',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {
            'text': 'Mesazhi',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Shkruani mesazhin tuaj...'}),
        }


class ContactForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True, label='Pranoj politiken e privatesise')

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'interest', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }
        labels = {
            'name': 'Emri',
            'email': 'Email',
            'phone': 'Telefoni',
            'interest': 'Interesi',
            'subject': 'Subjekti',
            'message': 'Mesazhi',
        }

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_subject(self):
        return self.cleaned_data['subject'].strip()

    def clean_message(self):
        return self.cleaned_data['message'].strip()
