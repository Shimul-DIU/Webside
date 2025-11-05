
from django.shortcuts import render
from Blog.models import Bloginfo
# Create your views here.
def Binfo(request):
    return render(request,'Blog/blog.html')
def FormInfo(request):
    if request.method=='POST':
        dt=request.POST.get('date')
        lt=request.POST.get('location')
        bus=request.POST.get('Bus')
        motorcycle=request.POST.get('Motorcycle')
        bugati=request.POST.get('Bugatti')
        friend=request.POST.get('friends')
        
        vehicle=[]
        if bus:
            vehicle.append(bus)
        if motorcycle:
            vehicle.append(motorcycle)
        if bugati:
            vehicle.append(bugati)
        cars=' '.join(vehicle)

        Bloginfo.objects.create(
            date=dt,
            location=lt,
            vehicle=cars,
            friends=friend,
        )
    return render(request,'Blog/form.html')