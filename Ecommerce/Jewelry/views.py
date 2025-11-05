from django.shortcuts import render
from .models import Productinfo

def jinfo(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phoneNumber')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')

        Productinfo.objects.create(
            name=name,
            phoneNumber=phone,
            address=address,
            quantity=quantity
        )

        # Optional: success message দেখাতে চাইলে context এ পাঠাতে পারো
        return render(request, 'product.html', {'message': 'Your data has been saved successfully!'})

    return render(request, 'product.html')
