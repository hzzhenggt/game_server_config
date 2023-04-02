from django import forms
from .models import Server, ServerFile



class ServerFileForm(forms.ModelForm):
    class Meta:
        model = ServerFile
        fields = ['name', 'deploy_path', 'description', 'content']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 20}),
        }

    #content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter file name'})
        self.fields['deploy_path'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter deploy path'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description'})
        # self.fields['content'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Content'})



class ServerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    private_key_password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = Server
        fields = ('name', 'host', 'port', 'username', 'password', 'private_key', 'private_key_password')
        widgets = {
            'private_key': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        private_key = cleaned_data.get('private_key')
        private_key_password = cleaned_data.get('private_key_password')
        if not password and not private_key:
            raise forms.ValidationError('Either password or private key must be provided.')
        
        

