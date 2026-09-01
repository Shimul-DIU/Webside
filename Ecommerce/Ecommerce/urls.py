"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('man/', include('Man.urls')),
    path('women/', include('Women.urls')),
    path('blog/', include('Blog.urls')),
    path('hotoffers/', include('Hot_Offers.urls')),
    path('jewelry/', include('Jewelry.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# এই লাইনটা media ফাইল serve করার জন্য
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
