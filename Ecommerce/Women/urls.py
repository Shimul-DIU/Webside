from django.urls import path
from . import views
urlpatterns = [
    path('',views.women_info,name='women'),
    path('Product',views.display,name='product')
]
