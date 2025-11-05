from django.contrib import admin
from Hot_Offers.models import demo
class demoadmin(admin.ModelAdmin):
    list_display=('customerid','customerName','location','phone')
# Register your models here.
admin.site.register(demo,demoadmin)