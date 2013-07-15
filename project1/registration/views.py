# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime
from Rate.models import Person
from django import forms
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User
#for login
from django.contrib.auth import authenticate, login as auth_login, logout

class LoginForm(forms.Form):
	username=forms.CharField(max_length=20)
	password=forms.CharField(max_length=20, widget=forms.PasswordInput())

def login_user(request, next='/categories'):

	lForm=LoginForm()
	# if request.GET.has_key('next'):
	# 	next=request.GET['next']
	# 	print 'got here has key thing'
	if request.method=='POST':
		if request.POST['submit']=='login':
			postDict=request.POST.copy()
			lForm=LoginForm(postDict)
			if lForm.is_valid():
				uName=request.POST['username']
				uPass=request.POST['password']
				user=authenticate(username=uName, password=uPass)
				if user is not None:
					auth_login(request, user)
					return HttpResponseRedirect(next)
				else:
					print('login incorrect')
	args={}
	args.update(csrf(request))
	args['lForm']=lForm
	args['request']=request
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('registration/login.html', args)
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/login')


class NewUserForm(forms.Form):
	username=forms.CharField(max_length=30)
	password=forms.CharField(max_length=20, widget=forms.PasswordInput())
	first=forms.CharField(max_length=20)
	last=forms.CharField(max_length=20)
	email=forms.EmailField(max_length=30)

def create_user(request):
	uForm=NewUserForm()
	if request.method=='POST':
		if request.POST['submit']=='create':
			postDict=request.POST.copy()
			uForm=NewUserForm(postDict)
			try:
				#create user object
				user=User.objects.create_user(postDict['username'], postDict['email'], postDict['password'])
				user.save()
				print 'successfully created new user'
				person=Person(user=user)
				person.save()
				print 'created a person for this user'
			except:
				print 'user creation error'
	args={}
	args.update(csrf(request))
	args['uForm']=uForm
	args['request']=request
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('registration/create_user.html', args)