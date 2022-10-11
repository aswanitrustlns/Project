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
#Manage Account page
def manage_account(request):
    if 'UserId' in request.session:
        nationality=selector.load_nationality()
        country=selector.loadCountry()
        leverage=selector.loadLeverage()
        accountType=selector.loadAccountType()
        risk=selector.loadRiskCategory()
        return render(request,'backoffice/officemanagement.html',{"nations":nationality,'country':country,'leverage':leverage,'account':accountType,'risks':risk}) 
    else:
        return redirect('/login')

#Load account details
def load_account_details(request):
    if 'UserId' in request.session:
        acc_no=request.GET.get('account')
        details=selector.loadAccountDetails(acc_no)
        return JsonResponse({"detail":details}) 
    else:
        return redirect('/login')
#Duplicate check
def check_duplicate(request):
    if 'UserId' in request.session:
        acc_no=request.GET.get('account')
        duplicate=selector.duplicate_account(acc_no)
        return JsonResponse({"duplicate":duplicate}) 
    else:
        return redirect('/login')
#Update Back office
def backoffice_update(request):
    if 'UserId' in request.session:
        msg=""
        acc_no=request.POST.get('accno')
        leverage=int(request.POST.get("Leverage"))
        category=selector.duplicate_account(acc_no)
        if(category=="RC" and leverage>30):
            msg="Retail clients cannot have leverage greater than 30"
        else:
            service.update_details(request)
        return JsonResponse({"msg":msg}) 
    else:
        return redirect('/login')




