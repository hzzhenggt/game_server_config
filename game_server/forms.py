from django import forms
from .models import Server


class ServerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Server
        fields = ('name', 'host', 'port', 'username', 'password', 'private_key')
        widgets = {
            'private_key': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        private_key = cleaned_data.get('private_key')
        if not password and not private_key:
            raise forms.ValidationError('Either password or private key must be provided.')

