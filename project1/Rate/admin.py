from django.contrib import admin
from Rate.models import Entry, Category, Person, Rating, Comment

admin.site.register(Entry)
admin.site.register(Category)
admin.site.register(Person)
admin.site.register(Rating)
admin.site.register(Comment)