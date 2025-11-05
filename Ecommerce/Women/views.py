from django.shortcuts import render
from .models import Women_info
# Create your views here.
def women_info(request):
    return render(request,'Women/women.html')
def display(request):
    if request.method=='POST':
        qn=request.POST.get('quantity')
        nm=request.POST.get('name')
        pn=request.POST.get('phone')
        ad=request.POST.get('address')
        pname=request.POST.get('pname')

        Women_info.objects.create(
         orderNumber=qn,
         personName=nm,
         phoneNumber=pn,
         address=ad,
         productName=pname,
         
        )
        
    return render(request,'Women/products.html')