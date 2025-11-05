from django.urls import path
from . import views

urlpatterns = [
  path('details/',views.Binfo, name='blog'),
  path('bform/',views.FormInfo, name='blog_form')
  
]