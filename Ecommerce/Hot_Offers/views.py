from django.shortcuts import render

# Create your views here.
def hinfo(request):
    return render(request,'Hotoffers/hotoffer.html')