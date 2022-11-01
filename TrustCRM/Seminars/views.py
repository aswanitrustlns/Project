from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .services import Services
service=Services()
# Create your views here.
def view_seminars(request):
    if 'UserId' in request.session:
        
        titles=service.get_last_seminar()
        
        last_seminar=service.get_seminars_last()
        all_seminar=service.get_seminar_info_list()
        return render(request,'seminars/eventregistration.html',{'titles':titles,'seminars':all_seminar,'last':last_seminar})
    else:
         return redirect('/login') 
#view seminar report
def view_seminar_report(request):
    if 'UserId' in request.session:
        seminarList=service.get_seminar_details()
        last_seminar=service.get_seminars_last()
        
        print("Last seminar======",last_seminar)
        if last_seminar:
            seminar_id=last_seminar[0]
        print("Last seminar Id=======",seminar_id)
        lastseminar_grid=service.load_seminar_grid(seminar_id) 
        webinar_info=service.view_webinar(seminar_id)   
        seminar_count=service.get_seminar_count(seminar_id)
        return render(request,'seminars/seminarreport.html',{"details":seminarList,'grids':lastseminar_grid,'webinarInfo':webinar_info,'count':seminar_count})
    else:
         return redirect('/login') 
def add_button_click(request):
    if 'UserId' in request.session:
        print("Add button click")
        service.save_new_event_details(request)
        return JsonResponse({"saved":"success"})
    else:
         return redirect('/login')
def get_webinar_info(request):
    if 'UserId' in request.session:
        webinarid=request.GET.get('id')
        webinarinfo=service.view_webinar(webinarid)
        return JsonResponse({"info":webinarinfo})
    else:
         return redirect('/login')
def edit_button_click(request):
    if 'UserId' in request.session:
        service.update_event_details(request)
        return JsonResponse({"saved":"success"})
    else:
         return redirect('/login')
def delete_seminar(request):
    if 'UserId' in request.session:
        id=request.GET.get('id')
        service.delete_seminar(id)
        return JsonResponse({"delete":"success"})
    else:
         return redirect('/login')
def report_load(request):

    if 'UserId' in request.session:
        seminar_id=request.GET.get('id')
        print("Seminar I===========",seminar_id)
        lastseminar_grid=service.load_seminar_grid(seminar_id) 
        webinar_info=service.view_webinar(seminar_id)   
        seminar_count=service.get_seminar_count(seminar_id)
        return JsonResponse({"grid":lastseminar_grid,"info":webinar_info,'count':seminar_count})
    else:
         return redirect('/login')

def view_opened_account(request):
  
    if 'UserId' in request.session:
        fromdate=request.GET.get('from')
        todate=request.GET.get('to')
        grid_data=service.get_accounts_opened(fromdate,todate)
        print("Grid data=============",grid_data)
        return JsonResponse({"grid":grid_data})
    else:
         return redirect('/login')

def update_account(request):
  
    if 'UserId' in request.session:
        print("Attendence update======")
        userid=request.session.get('UserId')
        ticket=request.GET.get('ticket')
        status=request.GET.get('status')
        seminarid=request.GET.get('seminarid')
        print("Data=================",ticket,status,seminarid,userid)
        
        service.update_attending_status(ticket,status,seminarid,userid)
        seminar_grid=service.load_seminar_grid(seminarid)
        return JsonResponse({"grid":seminar_grid})
    else:
         return redirect('/login')

def print_attendees(request):
    if 'UserId' in request.session:
        seminarid=request.GET.get('seminar')
        attendees=service.get_seminar_report(seminarid)
        print("Attendees=====",attendees)
        return render(request,"seminars/printattendees.html",{"attendees":attendees})
    else:
         return redirect('/login')

def seminar_confirmation(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        nationality=service.load_nationality()
        sources=service.load_source_list()
        salesrep=service.get_salesrep_permission(userid)
        country=service.loadCountry()
        upcoming_seminars=service.get_upcoming_seminar()
        return render(request,"seminars/seminarconfirmation.html",{'nationality':nationality,'sources':sources,'reps':salesrep,'countries':country,'upcoming':upcoming_seminars})
    else:
         return redirect('/login')
#Register seminars
def registerSeminars(request):  
    if 'UserId' in request.session:
        
        userid=request.session.get('UserId')
        title=request.GET.get('title')
        name=request.GET.get('name')
        to_addr=request.GET.get('to_addr')
        seminartitle=request.GET.get('seminartitle')
        ticket=request.GET.get('ticket')
        message=service.register_seminar(title,name,to_addr,seminartitle,ticket,userid)
                                           
        return JsonResponse({"msg":message})
    else:
       return JsonResponse({"msg":"Your session expired! Please login to continue"}) 
def confirmation_grid(request):
    if 'UserId' in request.session:
        load_data=service.load_confirmation_grid(request)
        print("Load data======",load_data)
        return JsonResponse(load_data,safe=False)    
    else:
         return redirect('/login')
    
#send email template
def send_email_templates(request):
    print("send email=======")
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        fromaddr=request.GET.get('from')
        to=request.GET.get('to')
        name=request.GET.get('name')
        title=request.GET.get('tit')
        lang=request.GET.get('lan')
        sub=request.GET.get('sub')
        ticket=request.GET.get('ticket')
        salesrep=request.GET.get('rep')
        print("Template selectio=====",lang,sub,fromaddr,to,title,name,userid,ticket,salesrep)
        service.email_template_selection(lang,sub,fromaddr,to,title,name,userid,ticket,salesrep)
        return JsonResponse({"success":"Email Send"})
    else:
        return JsonResponse({"success":"Your session expired! Please login to continue"})

def upcoming_details(request):
    if 'UserId' in request.session:
        seminarid=request.GET.get('id')
        details=service.upcoming_seminar_details(seminarid)
        print("Load data======",details)
        return JsonResponse({"details":details})    
    else:
         return redirect('/login')


    

