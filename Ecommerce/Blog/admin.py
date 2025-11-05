from django.contrib import admin
from .models import Bloginfo
class adminBlog(admin.ModelAdmin):
    list_display=('date','location','vehicle','friends')
# Register your models here.
admin.site.register(Bloginfo,adminBlog)