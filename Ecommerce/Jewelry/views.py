from django.shortcuts import render
from Home.models import Product
from .models import Productinfo

def jinfo(request):
    products = Product.objects.filter(category='jewelry', is_active=True).order_by('-created_at')

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phoneNumber')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')

        Productinfo.objects.create(
            name=name,
            phone=phone,
            address=address,
            quantity=quantity
        )

        return render(request, 'Jewelry/product.html', {
            'message': 'Your data has been saved successfully!',
            'products': products
        })

    return render(request, 'Jewelry/product.html', {'products': products})
