from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class ContactForm(forms.Form):
	fullName=forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control",
		"id":"full-name",
		"placeholder":"your name"
		}))
	Email=forms.EmailField(widget=forms.EmailInput(attrs={
		"class":"form-control",
		"id":"email-id",
		"placeholder":"xyz@gmail.com"
		}))
	Content=forms.CharField(widget=forms.Textarea(attrs={
		"class":"form-control",
		"id":"content-id",
		"placeholder":"write your content..."
		}))


	def clean_Email(self):
		email = self.cleaned_data.get("Email")
		if "gmail.com" not in email:
			raise forms.ValidationError("Email has to be gmail.com")
		return email
		


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


	def clean_username(self):
		username=self.cleaned_data.get("username")
		qs=User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("username exists!!")
		return username

	def clean_email(self):
		email=self.cleaned_data.get("email")
		qs=User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email exits!!")
		return email

	def clean(self):
		password=self.cleaned_data.get("password")
		password2=self.cleaned_data.get("password2")
		if password!=password2:
			raise forms.ValidationError("password do not match!!")
		return password