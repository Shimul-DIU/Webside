
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .models import Oderinfo

def display(request):
    return render(request,'Home/index.html')
def order(request):
    name=request.GET.get('name')
    img=request.GET.get('img')
    tk=request.GET.get('tk')
    if request.method == 'POST':
        uname = request.POST.get('name')
        phone = request.POST.get('phoneNumber')
        payment = request.POST.get('payment')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')

    
        Oderinfo.objects.create(
            name=uname,
            phone=phone,
            payment=payment,
            address=address,
            quantity=quantity
        )

    return render(request, 'Order.html', {'name': name, 'img': img, 'tk': tk})
def login_info(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            storage = messages.get_messages(request)
            storage.used = True 
            messages.error(request,'wrong password')
        
    return render(request,'loging.html')

def registrations(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,

        )
        user.is_staff=True
        user.save()
        return redirect('login')

    return render(request,'registration.html')