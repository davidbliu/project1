from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person
from django import forms
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory


def cat_list(request):
	cList=Category.objects.all()
	return render_to_response('Rate/category_list.html',{'categories': cList})

def entry_detail(request, eID='0', opts=()):
	entry=get_object_or_404(Entry, pk=eID)
	ratings=Rating.objects.all()
	score=0
	numRates=0
	for rate in ratings:
		if rate.entry==entry:
			score+=rate.score
			numRates+=1
	if (numRates !=0 ):
		score=score/numRates
	return render_to_response('Rate/entry_detail.html', {'entry':entry, 'score':score})
#not in use 
class imageForm(ModelForm):
	class Meta:
		model=Entry
		fields=['image']


class CustAddForm(ModelForm):
	class Meta:
		model=Entry	
		fields=['name', 'image', 'category','date_added','description']
		widgets={
			'name':forms.HiddenInput(),
			'category':forms.HiddenInput(),
			'date_added':forms.HiddenInput(),
			'description':forms.HiddenInput(),
		}
def add_view(request):
	forms=[]
	for i in range(0,10):
		form=CustAddForm(initial={'category': Category.objects.get(id=1)})
		forms.append(form)
	if request.method=='POST':
		print('post request made in add_view')
		print(request.POST['image'])
		entry=Entry(image=request.POST['image'], category=Category.objects.get(id=1))
		entry.save()
	print forms[0]
	c={}
	c['forms']=forms
	c.update(csrf(request))
	return render_to_response('Rate/add_images.html',c)

