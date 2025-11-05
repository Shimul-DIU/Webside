from django.contrib import admin
# from Women.models import Women_info
# class WomenAdmin(admin.ModelAdmin):
#     list_display=('orderNumber','personName','phoneNumber','address','productName','locals')

# admin.site.register(Women_info,WomenAdmin)``
from Women.models import Women_info
# # Register your models here.

class womenadmin(admin.ModelAdmin):
    list_display=('orderNumber','personName','phoneNumber','address','productName')
admin.site.register(Women_info,womenadmin)