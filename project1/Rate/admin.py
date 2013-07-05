from django.contrib import admin
from Rate.models import Entry, Category, Person, Rating

admin.site.register(Entry)
admin.site.register(Category)
admin.site.register(Person)
admin.site.register(Rating)