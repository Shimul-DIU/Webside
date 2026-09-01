from django.contrib import admin
from Jewelry.models import Productinfo

class ProductinfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'quantity')
    search_fields = ('name', 'address')
    list_filter = ('quantity',)

# Register your models here.
admin.site.register(Productinfo, ProductinfoAdmin)
