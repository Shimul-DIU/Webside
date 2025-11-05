from django.contrib import admin
from Jewelry.models import Productinfo
class productinfo(admin.ModelAdmin):
    list_display=('name','phoneNumber','product','address','quantity')
# Register your models here.
admin.site.register(Productinfo)
