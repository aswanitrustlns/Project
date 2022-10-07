from django.shortcuts import render
from asyncio import events
from distutils.log import error

from ipaddress import ip_address
from sqlite3 import Cursor
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .service import Services
from .selector import Selector


selector=Selector()
service=Services()


# Create your views here.
#change password

def change_password(request):
    if 'UserId' in request.session:
        
        return render(request,'backoffice/changepassword.html')
    else:
        return redirect('/login')
def generate_passwords(request):
    if 'UserId' in request.session:
       master_pwd,investor_pwd,phone_pwd=selector.generatepassword()
       print("Passwords================================",master_pwd,investor_pwd,phone_pwd) 
       return JsonResponse({"master":master_pwd,"investor":investor_pwd,"phone":phone_pwd})
    else:
        return redirect('/login')
def change_password_request(request):
    if 'UserId' in request.session:
        service.change_password(request)
        return JsonResponse({"success":"done"})
    else:
        return redirect('/login')

