# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render_to_response, get_object_or_404
# from Rate.models import Category, Entry, Rating, Person
# from django import forms
# from django.forms import ModelForm
# from django.template import RequestContext
# from django.core.context_processors import csrf
# from django.forms.formsets import formset_factory

# # images imports
# import os
# import sys
# import time
# from urllib import FancyURLopener
# import urllib2
# import simplejson

# class EntryForm(ModelForm):
# 	def process(self):
# 			print 'processing the form'
# 			img= self.cleaned_data['image']
# 			cat=self.cleaned_data['category']
# 			entry=Entry(image=img, category=cat)
# 			entry.save()
# 			return HttpResponseRedirect('/entry/%s' % entry.id)
# 	class Meta:
# 		model=Entry	
# 		fields=['name', 'image', 'category','description']
# 		widgets={
# 			'image':forms.HiddenInput(),
# 			'name':forms.HiddenInput(),
# 			'category':forms.HiddenInput(),
# 			# 'date_added':forms.HiddenInput(),
# 			'description':forms.HiddenInput(),
# 		}
		
# def add_view(request, searchTerm='asdf', numForms=7, catID=1):
# 	print('im in the ad view in iviews term was: '+searchTerm)
# 	# searchTerm = "fruit"
# 	numForms=float(numForms)
# 	# Replace spaces ' ' in search term for '%20' in order to comply with request
# 	searchTerm = searchTerm.replace(' ','%20')
# 	urls=[]
# 	# Set count to 0
# 	count = 0
# 	for i in range(0,10): #2 pages of images (8)
# 	    # Notice that the start changes for each iteration in order to request a new set of images for each loop
# 	    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
# 	    # print url
# 	    req = urllib2.Request(url, None, {'Referer': 'testing'})
# 	    response = urllib2.urlopen(req)

# 	    # Get results using JSON
# 	    results = simplejson.load(response)
# 	    data = results['responseData']
# 	    dataInfo = data['results']

# 	    # Iterate for each result and get unescaped url
# 	     # print myUrl['unescapedUrl']
# 	    for myUrl in dataInfo:
# 	        if count<numForms:
# 		        print myUrl['unescapedUrl']
# 		        count = count + 1
# 		        urls.append(myUrl['unescapedUrl'])
# 	    # Sleep for one second to prevent IP blocking from Google
# 	    # time.sleep(.5)
# 	    if count>=numForms:
# 	    	break
# 	#end of getting image urls
# 	forms={}
# 	for url in urls:
# 		form=EntryForm(initial={'category': Category.objects.get(id=catID), 'image':url})
# 		forms[url]=form

# 	if request.method=='POST':
# 		# print('a post request was made')
# 		pForm=EntryForm(request.POST.copy())
# 		print(request.POST.copy())
# 		# print 'printing image twice'
# 		# print pForm['image']
# 		# pForm['image']=request.POST['image']
# 		# print pForm['image']
# 		# if pForm.is_valid():
# 		# 	pForm.cleaned_data['image']=request.POST['image']
# 		# 	pForm.process()
# 		# else:
# 		# 	print(pForm.errors)
# 		# 	print('there was a problem with is valid the form')
# 		# pForm=EntryForm(request.POST)
# 		# img=request.POST['image']

# 		# entry=Entry(category=Category.objects.get(id=1), image=img)
# 		# entry.save()
# 		# return HttpResponseRedirect('/entry/%s' % entry.id)
# 	c={}
# 	c['forms']=forms
# 	c['urls']=urls
# 	c.update(csrf(request))
# 	return render_to_response('Rate/changedb.html',c)
