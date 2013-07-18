# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment, Saved
from chat.models import Message
import decimal
from decimal import *
from django import forms
from datetime import datetime
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User


def messages_view(request):
	my_messages={}
	senders=[]
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	me=Person.objects.get(user=request.user)
	friends=me.friends.all()
	if request.method=='POST':
		if request.POST.get('send') is not None:
			name=request.POST.get('friends_select')
			reciever=User.objects.get(username=name)
			message=Message(message=request.POST.get('message_text'), sender=request.user, reciever=reciever)
			message.save()
			print 'successfully sent message'
	me=Person.objects.get(user=request.user)
	inbox=Message.objects.filter(reciever=request.user)
	inbox=inbox.order_by('added').reverse()
	for m in inbox:
		sender=Person.objects.get(user=m.sender)
		my_messages[m]=sender
	args={}
	args.update(csrf(request))
	args['friends']=friends
	args['messages']=my_messages
	args['request']=request
	if request.user.is_authenticated():
		args['person']=Person.objects.filter(user=request.user)[0]
	return render_to_response('chat/message_view.html', args)
