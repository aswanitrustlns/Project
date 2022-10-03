from django.shortcuts import render
from .services import Services
service=Services()
# Create your views here.
def view_seminars(request):
    seminars=service.get_seminars()
    return render(request,'')
