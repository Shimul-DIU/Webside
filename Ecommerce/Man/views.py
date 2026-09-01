from django.shortcuts import render
from Home.models import Product

def homepage(request):
    products = Product.objects.filter(category='men', is_active=True).order_by('-created_at')
    return render(request, 'Man/man.html', {'products': products})
