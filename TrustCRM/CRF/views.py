from django.shortcuts import redirect, render
from .models import TblCasetypes,TblUser,TblPriority,TblCases
from django.http import HttpResponse, JsonResponse
from datetime import datetime,timedelta
import string
import random

# Create your views here.
def case_report(request):
    if 'UserId' in request.session:
        cases=TblCases.objects.all().using('crf')
        return render(request,'crf/case-details.html',{'cases':cases})
    else:
        return redirect('/login')
def case_register(request):
    if 'UserId' in request.session:
        assigns=TblUser.objects.using('crf').filter(membertype='SUPER USER')
        casetype=TblCasetypes.objects.all().using('crf')
        priority=TblPriority.objects.all().using('crf')
        return render(request,'crf/case-register.html',{'types':casetype,'priors':priority,'assigns':assigns})
    else:
        return redirect('/login')
def case_datefilter(request):
    if 'UserId' in request.session:
        fromdate=request.GET.get('from')
        todate=request.GET.get('to')
        print("From date To date=====",fromdate,todate)
        cases=TblCases.objects.using('crf').filter(modified__gte=fromdate,modified__lt=todate).values()    
        print("Cases====",list(cases))
        return JsonResponse(list(cases),safe=False)
    else:
        return redirect('/login')
def detailed_page(request):
    if 'UserId' in request.session:
        return render(request,'crf/details.html')
    else:
        return redirect('/login')
def save_case(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        assigneddpt=request.POST.get('assignedto')
        casetype=request.POST.get('casetype')
        priority=request.POST.get('priority')
        topic=request.POST.get('topic')
        description=request.POST.get('textdescription')
        assign=request.POST.get('assign')
        if(assign=="manager"):
            assignedto=11
            status="Management Aprroval Pending"
        else:
            assignedto=10
            status="Pending"
        companyid=5
        comments=""
        nums=random.randrange(1, 10**3)
        casecode="TRSVG"+str(UserId)+"_"+str(nums)
        print("Case code=====",casecode)
        
        regdate=datetime.today().date()
        
        registercase=TblCases(1,casecode,topic,description,priority,UserId,regdate,regdate,assigneddpt,casetype,assignedto,companyid,status,comments)
        registercase.save(using='crf')
        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')


# def login_user_info(logedUsername):
#     userInfo=TblUser.objects.using('crf').filter(username=logedUsername)
#     print("UserInfo======",userInfo)
#     return userInfo