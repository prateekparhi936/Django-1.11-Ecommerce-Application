from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class GuestForm(forms.Form):
		email=forms.EmailField()

class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control",
		"id":"username",
		"placeholder":"username"
		}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"id":"password",
		"placeholder":"password"
		}))


class RegisterForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={
		 "class":"form-control",
		 "id":"username",
		 "placeholder":"enter a username"
		}))
	email=forms.EmailField(widget=forms.EmailInput(attrs={
		"class":"form-control",
		"id":"emailid",
		"placeholder":"xyx@gmail.com"
		}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"id":"password",
		"placeholder":"enter a password(including alphabet and numeric (length>=8)"
		}))
	password2=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"id":"password2",
		"placeholder":"confirm password"
		}))