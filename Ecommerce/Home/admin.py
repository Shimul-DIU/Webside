from django.contrib import admin
from django.contrib import admin
from Home.models import Oderinfo
class demoadmin(admin.ModelAdmin):
    list_display=('name','phone','payment','address','quantity')
# Register your models here.
admin.site.register(Oderinfo,demoadmin)