from django.urls import path
from . import views
urlpatterns = [
    path('',views.display,name='home'),
    path('login/',views.login_info,name='login'),
    path('register/',views.registrations,name='register'),
    path('order/',views.order,name='order'),

]
