from django.shortcuts import redirect, render
from .models import TblCasetypes,TblUser,TblPriority,TblCases,TblCasedetails,TblDocuments,TblCasesummary
from django.http import HttpResponse, JsonResponse
from datetime import datetime,timedelta,date
from django.utils import timezone
import string
import random
import os
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
        if(fromdate=="" and todate==""):
            cases=TblCases.objects.all().using('crf')
        else:
            cases=TblCases.objects.using('crf').filter(modified__gte=fromdate,modified__lt=todate)
        return render(request,'crf/case-details.html',{'cases':cases})
        # print("Cases====",list(cases))
        # return JsonResponse(cases,safe=False)
    else:
        return redirect('/login')
def detailed_page(request):
    if 'UserId' in request.session:
        case=request.GET.get('Case')
        print("Case details===="+case)
        casedetails=TblCasedetails.objects.using('crf').filter(caseid=case)
        docdetails=TblDocuments.objects.using('crf').filter(caseid=case)
        activities=[]
        for details in casedetails:
            print("Case detail Id====",details.casedetailid)
            activity=TblCasesummary.objects.using('crf').filter(casedetailid=details.casedetailid)
            print("Activity======",activity)
            activities.append(activity)
        print("Activities====",activities)
        return render(request,'crf/details.html',{"details":casedetails,"docs":docdetails,"activities":activities})
    else:
        return redirect('/login')


def save_case(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        assignedto=request.POST.get('assignedto')
        casetype=TblCasetypes()
        
        casetype_id=request.POST.get('casetype')
        casetype.id=casetype_id
        priority_id=request.POST.get('priority')
        priority=TblPriority()
        priority.id=priority_id
        topic=request.POST.get('topic')
        description=request.POST.get('textdescription')
        assign=request.POST.get('assign')
        docfile=request.FILES.get("docfile",None)
        print("Assign====",assign)
        status="Pending"
        if(assign=="manager"):
            assignedto=11
            status="Management Aprroval Pending"
       
            
        assigned=TblUser()
        assigned.userid=assignedto
        companyid=5
        comments=""
        nums=random.randrange(1, 10**3)
        casecode="TRSVG"+str(UserId)+"_"+str(nums)
        print("Case code=====",casecode)
        
        regdate = datetime.now()
        
        print("Assigned To====",assignedto)
        registercase=TblCases(casecode=casecode,topic=topic,description=description,priority=priority,userid=UserId,regdate=regdate,modified=regdate,assigneddpt=1,casetype=casetype,assignedto=assigned,companyid=companyid,status=status,comments=comments)
        registercase.save(using='crf')

        registerid=TblCases.objects.using('crf').latest('caseid')
        print("registerid====",registerid.caseid)
        caseid=registerid.caseid
        completed=0
        registerdetail=TblCasedetails(caseid=caseid,topic=topic,description=description,regdate=regdate,modified=regdate,iscompleted=completed,completiondate=None,expcompletion=None,status=status,userid=assigned,priority=priority,casetype=casetype)
        registerdetail.save(using='crf')
        details=TblCasedetails.objects.using('crf').latest('casedetailid')
        detailid=details.casedetailid
        caseid=41
        detailid=26
        if docfile:
            imagedata=None
            extension1 = os.path.splitext(str(docfile))[1]
            imagename=os.path.splitext(str(docfile))[0]
            fullname=imagename+extension1
            file_path="static\\uploads\\"
                # file_path=os.path.join(UPLOAD_ROOT,accno)
            print("File existance======",file_path,os.path.isfile(file_path))
            if os.path.isfile(file_path):
                os.mkdir(file_path)
            fullpath=str(caseid)+extension1
            print("Full path====",fullpath)
            fullfilepath=os.path.join(file_path,fullpath)
            print("File",fullfilepath)
            with open(fullfilepath, 'wb+') as destination:
                for chunk in docfile.chunks():
                    imagedata=chunk
            if(extension1==".doc"):
                contenttype = "application/vnd.ms-word"
            if(extension1== ".docx"):
                contenttype = "application/vnd.ms-word"
            if(extension1==".xls"):
                contenttype = "application/vnd.ms-excel"
            if(extension1==".xlsx"):
                contenttype = "application/vnd.ms-excel"
            if(extension1==".jpg"):
                contenttype = "image/jpg"
            if(extension1==".JPG"):
                contenttype = "image/jpg"
            if(extension1==".JPEG"):
                contenttype = "image/jpg"
            if(extension1==".jpeg"):
                contenttype = "image/jpg"
            if(extension1==".png"):
                contenttype = "image/png"
            if(extension1==".PNG"):
                contenttype = "image/png"
            if(extension1==".gif"):
                contenttype = "image/gif"
            if(extension1==".GIF"):
                contenttype = "image/gif"
            if(extension1==".bmp"):
                contenttype = "image/bmp"
            if(extension1==".BMP"):
                contenttype = "image/bmp"
            if(extension1== ".pdf"):
                contenttype = "application/pdf"
            if(extension1==".PDF"):
                contenttype = "application/pdf"
            
            print("Type odf imagedata===",type(imagedata))
            docs=TblDocuments(caseid=caseid,casedetailid=detailid,casesummaryid=0,documentdata=imagedata,documentname=imagename,doctype=contenttype,uploadeddate=regdate)
            docs.save(using='crf')
        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')
def case_file_upload(request):
    if 'UserId' in request.session:
        caseid=request.POST.get('caseid')
        detail=TblCasedetails.objects.using('crf').get(caseid=caseid)
        print("Detail======")
        detailid=detail.casedetailid
        print("Detailid===",detailid)
        docfile=request.FILES.get("docfile",None)
        if docfile:
            imagedata=None
            extension1 = os.path.splitext(str(docfile))[1]
            imagename=os.path.splitext(str(docfile))[0]
            fullname=imagename+extension1
            file_path="static\\uploads\\"
                # file_path=os.path.join(UPLOAD_ROOT,accno)
            print("File existance======",file_path,os.path.isfile(file_path))
            if os.path.isfile(file_path):
                os.mkdir(file_path)
            fullpath=str(caseid)+extension1
            print("Full path====",fullpath)
            fullfilepath=os.path.join(file_path,fullpath)
            print("File",fullfilepath)
            with open(fullfilepath, 'wb+') as destination:
                for chunk in docfile.chunks():
                    imagedata=chunk
            if(extension1==".doc"):
                contenttype = "application/vnd.ms-word"
            if(extension1== ".docx"):
                contenttype = "application/vnd.ms-word"
            if(extension1==".xls"):
                contenttype = "application/vnd.ms-excel"
            if(extension1==".xlsx"):
                contenttype = "application/vnd.ms-excel"
            if(extension1==".jpg"):
                contenttype = "image/jpg"
            if(extension1==".JPG"):
                contenttype = "image/jpg"
            if(extension1==".JPEG"):
                contenttype = "image/jpg"
            if(extension1==".jpeg"):
                contenttype = "image/jpg"
            if(extension1==".png"):
                contenttype = "image/png"
            if(extension1==".PNG"):
                contenttype = "image/png"
            if(extension1==".gif"):
                contenttype = "image/gif"
            if(extension1==".GIF"):
                contenttype = "image/gif"
            if(extension1==".bmp"):
                contenttype = "image/bmp"
            if(extension1==".BMP"):
                contenttype = "image/bmp"
            if(extension1== ".pdf"):
                contenttype = "application/pdf"
            if(extension1==".PDF"):
                contenttype = "application/pdf"
            
            print("Type odf imagedata===",type(imagedata))
            regdate =datetime.now()
            docs=TblDocuments(caseid=caseid,casedetailid=detailid,casesummaryid=0,documentdata=imagedata,documentname=imagename,doctype=contenttype,uploadeddate=regdate)
            docs.save(using='crf')

        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')

def change_status(request):
    if 'UserId' in request.session:
        caseid=request.GET.get('id')
        status=request.GET.get('status')
        print("Deatails====",caseid,status)
        case=TblCases.objects.using('crf').get(caseid=caseid)
        case.status=status
        case.save(using='crf')
        print("Case====",case)
        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')
def reopen_case(request):
    if 'UserId' in request.session:
        caseid=request.GET.get('id')
        status=request.GET.get('status')
        description=request.GET.get('description')
        assign=request.GET.get('assign')
        print("Deatails====",caseid,status,description,assign)
        case=TblCases.objects.using('crf').get(caseid=caseid)
        case.status=status
        if(description!=""):
            case.description=description
        case.assigneddpt=assign
        case.save(using='crf')
        print("Case====",case)
        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')


def view_document(request):
    if 'UserId' in request.session:
        docid=request.GET.get('id')
        imagedetail=TblDocuments.objects.using('crf').filter(id=docid)
        contenttype=""
        imagetype=""
        imagename=""
        imagedata=""
        for detail in imagedetail:
            print("Image detail=====",detail.doctype)
            contenttype=detail.doctype
            imagetype=detail.doctype
            imagename=detail.documentname
            imagedata=detail.documentdata
        if(imagetype=="application/vnd.ms-word"):
                contenttype = ".doc"
        if(imagetype=="application/vnd.ms-word"):
            contenttype = ".docx"
        if(imagetype=="application/vnd.ms-excel"):
            contenttype = ".xls"
        if(imagetype=="application/vnd.ms-excel"):
            contenttype = ".xlsx"
        if(imagetype=="image/jpg"):
            contenttype =".jpg" 
        if(imagetype=="image/jpg"):
            contenttype = ".JPG"
        if(imagetype=="image/jpg"):
            contenttype = ".JPEG"
        if(imagetype=="image/jpg"):
            contenttype = ".jpeg"
        if(imagetype=="image/png"):
            contenttype = ".png"
        if(imagetype=="image/png"):
            contenttype =".PNG" 
            
        if(imagetype=="image/gif"):
            contenttype =".gif" 
                    
        if(imagetype=="image/gif"):
            contenttype =".GIF" 
        if(imagetype=="image/bmp"):
            contenttype = ".bmp"
        if(imagetype=="image/bmp"):
            contenttype = ".BMP"
        if(imagetype== "application/pdf"):
            contenttype = ".pdf"
        if(imagetype=="application/pdf"):
            contenttype = ".PDF"
        print("Content type====",contenttype)
        
        imagename=imagename+contenttype
        
        file_path="static\\uploads"+"\\"+imagename
        print("Image name=====",imagename)
        # with open('binary_file') as file: 
        #     data = file.read() 
        res = ''.join(format(x, '02x') for x in imagedata)
        result=str(res)
        data = bytes.fromhex(result) 
        with open(file_path, 'wb') as file: 
            file.write(data)
            
        return JsonResponse({"imagepath":file_path})
    else:
        return redirect('/login')
    
        



# def login_user_info(logedUsername):
#     userInfo=TblUser.objects.using('crf').filter(username=logedUsername)
#     print("UserInfo======",userInfo)
#     return userInfo