# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render_to_response, get_object_or_404
from Rate.models import Category, Entry, Rating, Person, Comment
# from django import forms
from datetime import datetime
# from django.forms import ModelForm
# from django.template import RequestContext
# from django.core.context_processors import csrf
# from django.forms.formsets import formset_factory

def get_friends_activities(person):
	friends=person.friends.all()
	ans=[]
	for rate in Rating.objects.all().order_by('updated').reverse():
		if rate.person in friends:
			ans.append(rate)
	for comment in Comment.objects.all().order_by('updated').reverse():
		if comment.person in friends:
			ans.append(comment)
	ans=sorted(ans, key=lambda object: object.updated, reverse=True)
	return ans
def get_my_rates(personer):
	ans=[]
	for rate in Rating.objects.all().order_by('score').reverse():
		if rate.person == personer:
			ans.append(rate)
	return ans
def filter_cats_by_term(term):
	ans=[]
	for cat in Category.objects.all():
		cat_name=cat.type
		if term in cat_name:
			ans.append(cat)
	return ans

def get_top_comment_dict(entries):
	ans={}
	for e in entries:
		tcomment=Comment.objects.filter(entry=e).order_by('likes').reverse()
		if tcomment:
			comments=[]
			for comment in tcomment:
				if len(comments) <10:
					comments.append(comment)
			# ans[e]=tcomment[0].comment
			ans[e]=comments
	return ans
