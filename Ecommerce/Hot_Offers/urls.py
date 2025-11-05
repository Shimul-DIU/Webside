from django.urls import path
from . import views

urlpatterns = [
  path('details/',views.hinfo, name='hotOffers')  
]