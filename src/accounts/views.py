from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail
# Create your views here.

def guest_login_page(request):
	guestForm=GuestForm(request.POST or None)
	context={
		"guestForm": guestForm
	}
	next_=request.GET.get('next')
	next_post=request.POST.get('next')
	redirect_path= next_ or next_post or None
	if guestForm.is_valid():
		email=guestForm.cleaned_data.get("email")	
		guest_email=GuestEmail.objects.create(email=email)
		request.session['guest_email_id']=guest_email.id
		if is_safe_url(redirect_path,request.get_host()):
			return redirect(redirect_path)
		else:
			return redirect("/register/")
	return redirect("/register/")




def login_page(request):
	loginForm=LoginForm(request.POST or None)
	context={
		"title":"Login Form",
		"loginForm": loginForm
	}
	context['loginForm']=LoginForm()
	next_=request.GET.get('next')
	next_post=request.POST.get('next')
	redirect_path= next_ or next_post or None
	if loginForm.is_valid():
		username=loginForm.cleaned_data.get("username")
		password=loginForm.cleaned_data.get("password")
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			try:
				del request.session['guest_email_id']
			except:
				pass
			if is_safe_url(redirect_path,request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		else:
			print("Error")
			#return redirect("/home_page")

	return render(request,"accounts/login.html",context)



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
	return render(request,"accounts/register.html",context)
