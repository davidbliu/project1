from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment
from django import forms
from datetime import datetime
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
import urllib
otherfile=open('imgsavereport.txt', 'w')
entries=Entry.objects.all()

# '{% static 'rate_page.css' %}
for e in entries:
	link=e.image
	filepath='static/images/imgdb/'
	filename = link.split('/')[-1]
	filename = filename.replace('/','')
	filename = filename.replace('%','')
	filename = filename.replace(';','')
	filename = filename.replace(':','')
	filename = filename.replace('-','')
	filename = filename.replace('#','')
	filename = filename.replace('@','')
	filename = filename.replace('.','')
	filename = filename.replace('%','')
	filename = filename.replace('{','')
	filename = filename.replace('\\','')
	filename = filename.replace('?','')
	filename = filename.replace('!','')
	filename = filename.replace(',','')
	filename = filename.replace('\n','')
	filename = filename.replace('_','')
	filename=filename+'.jpg'

	otherfile.write(filename)
	filepath=filepath+filename
	try:
		resource=urllib.urlopen(link)
		output=open(filepath, 'wb')
		output.write(resource.read())
		output.close()

		filepath = filepath.replace('static/','')
		e.image="{%  static \'"+filepath+"\' %}"
		e.save()
	except:
		print 'error'
otherfile.close()
