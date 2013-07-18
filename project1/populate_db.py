from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment
from django import forms
from datetime import datetime
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory

myfile=open('test.txt','r')

otherfile=open('test1.txt', 'w')
person=Person.objects.all()[0]
# category=Category.objects.all()[0]
# category=Category.objects.get(type='kpop')
category=Category(type='mass_added')
category.save()
line=myfile.readline()
while line != "" and line != None:
	try:
		e=Entry(added_by=person, image=line, category=category)
		e.save()
	except:
		otherfile.write('  problem:  ')
	otherfile.write(line)
	line=myfile.readline()




otherfile.write('and that was the last lineline')
otherfile.close()
myfile.close()