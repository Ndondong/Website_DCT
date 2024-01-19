from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.forms import FileInput


from .models import ModelPenyisipan, ModelPengekstrakan

class FormPenyisipan(forms.ModelForm):
	class Meta:
		model = ModelPenyisipan
		fields = ['host_img','wm_img',]
		widgets = {
			'host_img':FileInput(attrs={
				'class':'form-control',
				'onchange': "show_image(this, 'cover-image');",
				'accept':'image/*',
				}),
			'wm_img':FileInput(attrs={
				'class':'form-control',
				'onchange': "show_image(this, 'watermark-image');",
				'accept':'image/*',
				})
		}

class FormPengekstrakan(forms.ModelForm):
	class Meta:
		model = ModelPengekstrakan
		fields = ['host_img',]
		widgets = {
			'host_img':FileInput(attrs={
				'class':'form-control',
				'onchange': "show_image(this, 'cover-image');",
				'accept':'image/*',
				})
		}		

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
    	widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
    	widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(UserCreationForm):
	email = forms.EmailField(
		max_length=100,
		required = True,
		help_text='Enter Email Address',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		)
	username = forms.CharField(
		max_length=200,
		required = True,
		help_text='Enter Username',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
		)
	password1 = forms.CharField(
		help_text='Enter Password',
		required = True,
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
		)
	password2 = forms.CharField(
		help_text='Enter Password',
		required = True,
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
		)
	class Meta:
		model = User
		fields = [
			'username', 'email', 'password1', 'password2',
		]