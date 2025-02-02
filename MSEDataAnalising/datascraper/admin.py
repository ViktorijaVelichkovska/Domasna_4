from django.contrib import admin
from datascraper.models import  DayEntry, DayEntryAsString, Company

# Register your models here.
admin.site.register(DayEntry)
admin.site.register(DayEntryAsString)
admin.site.register(Company)