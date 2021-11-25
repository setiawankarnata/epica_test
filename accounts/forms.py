from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError

from pica.models import Company, Peserta
from .models import Profile


class LoginForm(AuthenticationForm):
    # company = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('profile2user', 'date_created', 'date_updated')
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bod': forms.Select(attrs={'class': 'form-control'}),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('profile2user', 'date_created', 'date_updated')
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'})
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        first_name = cleaned_data['first_name']
        if email == '' or None:
            self.add_error("email", "Email harus diisi!")
        if 'asmincoal.co.id' in email:
            pass
        else:
            if 'turanggaresources.com' in email:
                pass
            else:
                self.add_error("email", "Anda harus menggunakan email kantor")
        if first_name == '' or None:
            self.add_error("first_name", "First name tidak boleh dikosongkan")


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter Password'}),
        }

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if email == '' or None:
    #         raise ValidationError("Email tidak boleh dikosongkan!")
    #     return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        first_name = cleaned_data['first_name']
        if email == '' or None:
            self.add_error("email", "Email harus diisi!")
        if 'asmincoal.co.id' in email:
            pass
        else:
            if 'turanggaresources.com' in email:
                pass
            else:
                self.add_error("email", "Anda harus menggunakan email kantor")
        if first_name == '' or None:
            self.add_error("first_name", "First name tidak boleh dikosongkan")


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'})
        }


class PesertaForm(forms.ModelForm):
    class Meta:
        model = Peserta
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name peserta'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'peserta2company': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'bod': forms.NullBooleanSelect(attrs={'class': 'form-control', 'placeholder': 'BOD?'}),
        }
