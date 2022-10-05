from django.shortcuts import render
from .services import Services
service=Services()
# Create your views here.
def view_seminars(request):
    
    return render(request,'seminars/eventregistration.html')
