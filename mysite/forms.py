from django import forms
from .models import ContactSubmission, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'service', 'budget', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name', 'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@company.com', 'required': True,
            }),
            'service': forms.Select(),
            'budget': forms.Select(),
            'message': forms.Textarea(attrs={
                'placeholder': "Tell us a bit about what you're building...",
                'required': True,
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@company.com', 'required': True,
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        return email
