from django import forms

#from django.contrib.auth.models import User
from users.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=50, widget=forms.TextInput(
    attrs={
    'class': 'form-control', 'id': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(
    attrs={
    'class': 'form-control', 'id': 'email', 'placeholder': 'Example@hotmail.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
    attrs={
    'class': 'form-control'
    }))
    password2 = forms.CharField(label='Confirmar password',widget=forms.PasswordInput(
    attrs={
    'class': 'form-control'
    }
    ))

    #CON ESTE METODO, QUE VAMOS A IMPLEMENTAR UNA VALIDACION.
    def clean_username(self): #este metodo se va a ejecutar con is_valid()
        #OBTENEMOS INFO DEL INPUT USERNAME.
        username = self.cleaned_data.get('username')

        #CONSULTAMOS A BASE DE DATOS
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        else:
            return username


    def clean_email(self): #este metodo se va a ejecutar con is_valid()
        #OBTENEMOS INFO DEL INPUT USERNAME.
        email = self.cleaned_data.get('email')

        #CONSULTAMOS A BASE DE DATOS
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        else:
            return email

    #PARA UTILIZAR CLEAN, ES SOLAMENTE SI UN CAMPO DEPENDE DE OTRO
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')


    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
