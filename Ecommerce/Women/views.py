from django.shortcuts import render
from Home.models import Product
from .models import Women_info

def women_info(request):
    return render(request,'Women/women.html')

def display(request):
    products = Product.objects.filter(category='women', is_active=True).order_by('-created_at')

    if request.method=='POST':
        qn = request.POST.get('quantity')
        nm = request.POST.get('name')
        pn = request.POST.get('phone')
        ad = request.POST.get('address')
        pname = request.POST.get('pname')

        Women_info.objects.create(
            orderNumber=qn,
            personName=nm,
            phoneNumber=pn,
            address=ad,
            productName=pname,
        )

    return render(request,'Women/products.html', {'products': products})