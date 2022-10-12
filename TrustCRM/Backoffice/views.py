from email import message
from turtle import title
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
from .emailservice import EmailServices

selector=Selector()
service=Services()
emailservice=EmailServices()

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
#Load account details
def load_bankaccount_details(request):
    if 'UserId' in request.session:
        acc_no=request.GET.get('account')
        print("Account number=======",acc_no)
        details=selector.get_bank_details(acc_no)
        print("Details========",details)
        return JsonResponse({"details":details}) 
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
#Bank approval
def bank_approval(request):
    if 'UserId' in request.session:
        return render(request,"backoffice/bankapproval.html")
    else:
        return redirect('/login')

#load credit card data
def load_card_data(request):
    if 'UserId' in request.session:
        accno=request.GET.get('account')
        print("Account number=====",accno)
        details=selector.load_credit_card_details(accno)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            name=userdetails[1]
        
        return JsonResponse({"details":details,"name":name}) 
    else:
        return redirect('/login')
#Approve Card
def approve_card(request):
    if 'UserId' in request.session:
        status=request.GET.get('status')
        id=request.GET.get('id')
        userid=request.session.get('UserId')
        accno=request.GET.get('accno')
        card=request.GET.get('card')
        
        print("Account number=====",accno,card,status)
        details=selector.verify_redit_card_details(id,accno,status,userid)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            title=userdetails[2]
            name=userdetails[1]
            email=userdetails[0]
            emailservice.SendCardApprovalmail(title,name,email,card,"Credit",status)
        print("User details=========",userdetails)
        
        return JsonResponse({"details":details}) 
    else:
        return redirect('/login')
#Approve Bank
def approve_bank(request):
    if 'UserId' in request.session:
        print("Approve bank is here")
        status=request.GET.get('status')
        id=request.GET.get('id')
        userid=request.session.get('UserId')
        accno=request.GET.get('accno')
        card=request.GET.get('card')
        
        print("Account number=====",accno,card,status,id)
        details=selector.verify_bank_details(id,accno,status,userid)
        print("Detils-========",details)
        return JsonResponse({"details":details}) 
    else:
        return redirect('/login')
#Card Save
def save_card(request):
    if 'UserId' in request.session:
        message=""
        accno=request.POST.get('accno')
        count=selector.get_credit_card_count(accno)
        if count:
            count=count[0]
            print("Count==========",count)
            if(count>5):
                message="Cannot upload more than five Credit Cards"
        service.save_credit_card(request)
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')







