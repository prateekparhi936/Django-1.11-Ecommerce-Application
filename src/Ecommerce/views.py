
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import ContactForm, LoginForm, RegisterForm


def old_home_page(request):
	return HttpResponse("<b>HELLO WORLD</b>")


def home_page(request):
	context={
		"title":"Welcome to Home Page",
		"user":"GUEST"
	}
	if request.user.is_authenticated():
		context["user"]=request.user

	return render(request,"home_page.html",context)


def about_page(request):
	context={
		"title":"About Page Context"
	}
	if request.user.is_authenticated:
		context={
			"title":"New User"
		}
	return render(request,"home_page.html",context)



def contact_page(request):
	contactForm=ContactForm(request.POST or None)
	context={
		"title": "Contact Page Context",
		"contactForm": contactForm
	}
	if request.method=="POST":
		if contactForm.is_valid():
			print(contactForm.cleaned_data)
	return render(request,"contacts/view.html",context)



def login_page(request):
	loginForm=LoginForm(request.POST or None)
	context={
		"title":"Login Form",
		"loginForm": loginForm
	}
	print(request.user.is_authenticated())
	context['loginForm']=LoginForm()
	if request.method=="POST":
		if loginForm.is_valid():
			print(loginForm.cleaned_data)
			username=loginForm.cleaned_data.get("username")
			password=loginForm.cleaned_data.get("password")
			user=authenticate(request,username=username,password=password)
			if user is not None:
				print(request.user.is_authenticated())
				login(request,user)
				return redirect("/")
			else:
				#print("Error")
				return redirect("/home_page")

	return render(request,"auth/login.html",context)



User=get_user_model()
def register_page(request):
	registerForm=RegisterForm(request.POST or None)
	context={
		"title":"User Registration",
		"registerForm":registerForm
	}
	context["registerForm"]=RegisterForm()
	if request.method=="POST":
		if registerForm.is_valid():
			#print(registerForm.cleaned_data)
			username=request.POST["username"]
			email=request.POST["email"]
			password=request.POST["password"]
			new_user=User.objects.create_user(username,email,password,is_staff=True,is_superuser=True)
	return render(request,"auth/register.html",context)




def logout_page(request):
	if request.user.is_authenticated():
		logout(request)
	context={
		"title":"logged out"
	}
	return render(request,"auth/logout.html",context)