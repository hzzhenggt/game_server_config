from django import forms
from .models import Command, Server, ServerFile



class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['project', 'name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        content = cleaned_data.get('content')
        project = cleaned_data.get('project')
        if not name:
            raise forms.ValidationError('Name is required.')
        if not content:
            raise forms.ValidationError('Content is required.')
        if not project:
            raise forms.ValidationError('Project is required.')


class ServerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    private_key_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['password'].widget.attrs['autocomplete'] = 'off'
        # if self.instance:
        #     self.instance.password = None

    class Meta:
        model = Server
        fields = ['project', 'name', 'host', 'port', 'username', 'password', 'private_key', 'private_key_password']
        widgets = {
            'private_key': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        private_key = cleaned_data.get('private_key')
        private_key_password = cleaned_data.get('private_key_password')
        project = cleaned_data.get('project')
        #这里不能这样做，不然用户无法删除密码和私钥的密码
        # if password is None or password.strip() == '':
        #     original_instance = self.instance
        #     if original_instance.pk:
        #         cleaned_data['password'] = original_instance.password
        # if private_key_password is None or private_key_password.strip() == '':
        #     original_instance = self.instance
        #     if original_instance.pk:
        #         cleaned_data['private_key_password'] = original_instance.private_key_password
        if not password and not private_key:
            raise forms.ValidationError('Password or Private Key is required.')
        if not project:
            raise forms.ValidationError('Project is required.')
        return cleaned_data


        
    

class ServerFileForm(forms.ModelForm):
    class Meta:
        model = ServerFile
        fields = ['project', 'name', 'deploy_path', 'description', 'content']
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

    
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        name = cleaned_data.get('name')
        deploy_path = cleaned_data.get('deploy_path')
        content = cleaned_data.get('content')
        if not name:
            raise forms.ValidationError('Name is required.')
        if not project:
            raise forms.ValidationError('Project is required.')
        if not deploy_path:
            raise forms.ValidationError('Deploy path is required.')
        if not content:
            raise forms.ValidationError('Content is required.')


        
        



