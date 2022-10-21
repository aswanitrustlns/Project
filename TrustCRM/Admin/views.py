from asyncio import events
from distutils.log import error

from ipaddress import ip_address
from sqlite3 import Cursor
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session

from gtts import gTTS
import os
import json
import instaloader

import Admin

from .dashboard_selectors import DashboardSelector
from .services import Services
from .selectors import Selector

insta_username = "Tc_limited"
insta_password = "T@Cmited21!!"
all_data={}

# Load_Insta=instaloader.Instaloader()
Cursor=connection.cursor()
selector=Selector()
service=Services()
sales_dash=DashboardSelector()
global voice
global adminrole
adminrole="unset"
voice="False"
# Create your views here.

def login(request):    
    
    msg=" "
    return render(request,'admin/login.html',{'login_error':msg})

def login_check(request):
    global voice
    global adminrole
    print("login-start",datetime.now().time())
    msg="Username and Password do not match"
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        server_name=request.POST.get('servername')
        print("login=====",username,server_name,password)
    try:  
           
        UserId=selector.get_loged_user_info(username)  
        print("User Id==================",UserId,type(UserId))
        request.session['UserId'] = UserId
        if UserId==21:
            print("Admin login===================================")
            adminrole="admin" 
            request.session['role']="manager"
        else:
            adminrole="sales" 
            request.session['role']="salesrep"
        # request.session['UserId'] = 30
        connect=selector.exe_connection(username,server_name,password)
        
    except Exception as e:
        print("Exception------------",e.__class__)
        connect=1
        msg="User not Found"
        request.session["message"]=msg        
   
    print(connect)
    if(connect==0): 
            request.session['user']=username
            request.session['server']=server_name
            request.session['password']=password
            voice="True"            
            return redirect('dashboard/')
            # return redirect('salesdashboard/')
    else:
        request.session["message"]=msg
        return render(request,'admin/login.html',{'login_error':msg})

# def salesdashboard(request):
#     if 'UserId' in request.session:
#         UserId=request.session.get('UserId')
#         print("sales dashboard procedure start",datetime.now().time())
#         dashbord_data=sales_dash.sales_dashboard(UserId)     
#         print("sales dashboard procedure end",datetime.now().time()) 
#         return render(request,'sales/dashboard.html',dashbord_data)
#     else:
#         return redirect('/login')


def dashboard(request):
    
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        selrep=request.GET.get('repId')
        if(selrep!=None):
            UserId=selrep
        # else:
        #     UserId=request.session.get('UserId')
       
        
       
        permission_check=selector.user_role_selection(UserId)    

        manager=permission_check[11]
        salesRep=permission_check[22]
        print("Manager======================================",manager)
        print("Sales Rep===================================",salesRep)
        dashbord_data={}
        UserName,Email=selector.get_user_name(UserId)
        notification_count,notification=selector.get_notification_data(UserId)       
        request.session['UserId'] = UserId
        request.session['UserName']=UserName
        request.session['Email']=Email
        request.session['notification'] = notification_count
        request.session['notification_data']=notification
        global adminrole
        global voice       
        if voice=="True":
            mytext = 'Hi '+UserName+' Welcome to Trust Capital CRM'         
            print("My speech text=====",mytext)
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("static\\audio\\welcome.mp3")

        if voice=="False":
            if os.path.isfile("static\\audio\\welcome.mp3"):
                os.remove("static\\audio\\welcome.mp3")
                
           
        voice="False"
        
            # dashbord_data=sales_dash.sales_dashboard(UserId)     
            # print("sales dashboard procedure end",datetime.now().time()) 
            # return render(request,'sales/dashboard.html',dashbord_data)
        print("Admin value============================",adminrole)
        if manager:
                          
            
             print("Role============================manager")
            #  dashbord_data=sales_dash.admin_dashboard(UserId)  
             dashbord_data=sales_dash.manager_dashboard(UserId)    
             print("dashboard procedure ",datetime.now().time()) 
            #  return render(request,'sales/dashboard.html',dashbord_data)
             return render(request,'sales/managerdashboard.html',dashbord_data)
        if salesRep:
            
             
             dashbord_data=sales_dash.sales_dashboard(UserId)     
             print("sales dashboard procedure end",datetime.now().time()) 
             return render(request,'sales/dashboard.html',dashbord_data)
    else:
         return redirect('/login') 


   
def lead(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        print(UserId)
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        print("From date-----------------",from_date)
        print("To date------------------",to_date)
             
        lead="lead"
        leads_data,leads_count=selector.get_leads(lead,from_date,to_date)
        # print("Leads data---------------------",leads_data)
        return render(request,'sales/Leads.html',{'leads_data':leads_data,'leads_count':leads_count})
    else:
         return redirect('/login') 

def lead_load_all(request): 
    
    lead="all"
    from_date=request.GET.get('from')
    to_date=request.GET.get('to')
    print("From date-----------------",from_date)
    print("To date------------------",to_date)
    load_data,leads_count=selector.get_leads(lead,from_date,to_date)   
    # paginator = Paginator(load_data, 10)
    print("Load all data-------")
    print("load data-------------------------",len(load_data))
    return JsonResponse(load_data, safe=False)

def lead_load_click(request): 
    
    status=request.GET.get('status')  
    count=request.GET.get('count')
    if count:
        count=int(count)
    print("status===========================",status)
    print("Count++++++++++++++",count)  
    leads_data=selector.get_leads_clicks(status,count)   
    # paginator = Paginator(load_data, 10)
    print("Load all data-------")
    print("load data-------------------------",len(leads_data))
    return JsonResponse(leads_data, safe=False)
   

# def new_accounts(request):
#     if 'UserId' in request.session:
#         new_accounts_data=selector.get_new_accounts()
#         print("New Accounts page data")
#         # return render(request,'admin/newaccounts.html',{'page_data':new_accounts_data})
#     else:
#          return redirect('/login')

def lead_duplicate_check(request):
    print("Duplicate check-----------------------")
    phone=request.GET.get('phone')
    email=request.GET.get('email')
    print("Duplicate check-----------------------",phone,email)
    duplicate=selector.check_duplicate(phone,email)
    print("duplicate dataaaaaaaaaaaaa",duplicate)
    if duplicate:
        return JsonResponse({"success":True,"duplicate":duplicate})
    else:
        return JsonResponse({"success":False})

def view_merge(request):
    print("Request---------------------------")
    demoid=request.GET.get('demoid')
    ticket=request.GET.get('ticket')
    email1=request.GET.get('email1')
    email2=request.GET.get('email2')
    mobile=request.GET.get('mobile')
    telephone=request.GET.get('telephone') 
    print("Request---------------------------",demoid,ticket,email1,email2,mobile,telephone)
    selector.merge_ticket(ticket,email1,email2,mobile,telephone) 
    selector.close_lead(demoid,ticket)
    return JsonResponse({'success':True})

def create_ticket(request):
    print("create ticket")
    demoid=request.GET.get('id')
    print("demo iddd-----",demoid)
    email,phone=service.create_ticket_service(request)
    print("Ticket data---------------------------------")
    return JsonResponse({"success":True,"email":email,"phone":phone})    

def lead_registration(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')      
        UserName,Email=selector.get_user_name(UserId)        
        return render(request,'sales/LeadRegistration.html',{"source":UserName})
    else:
         return redirect('/login') 

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def lead_registration_check(request):
    
    UserId=request.session.get('UserId') # Read Session data
    
    if is_ajax(request=request):            
      
       
        try:  

            ticket=service.lead_registration(request,UserId)  
            email1=request.POST.get('email1')
            email2=request.POST.get('email2')
            mobile=request.POST.get('mobile')
            telephone=request.POST.get('telephone')           
            
            ticket=ticket[0]
            hash_check=ticket.find("#")
            ticket=ticket.replace('#','')
            print(hash_check)
            if hash_check>=0:    
                selector.merge_ticket(ticket,email1,email2,mobile,telephone)                
                
            login=0   
            user_permission=selector.user_permission_check(UserId,ticket,login)
            print("User Permissio-------",user_permission)
            user_permission=user_permission[0]                  
                    
                
            print("User Permissio-------",user_permission)
            if user_permission:
                print("No permission")
                return JsonResponse({'success':True,'ticket':ticket})
            else:
                print("permission")
                return JsonResponse({'success':False,'ticket':ticket})
        except:
            print("Error")
    
                
            
    else:
            
             return render(request,'admin/LeadProcessing.html')
            
        # print(merge_ticket)
        
def lead_processing(request):

    if 'UserId' in request.session:
        UserId=request.session['UserId']
        search_email_phone=[]
        search_email_phone1=[]
        search_email_phone2=[]
        search_email_phone3=[]
        page_data={}
        ticket=" "
        country_list=""
        accountno=""
        seminarlist=""
        webinars=""
        webinarList=[]
        seminar_list=[]
        email=request.session.get("Email")
        # count,itemsList=selector.template_send_items_list(email)
        try:
            ticket=request.GET.get('ticket')
            email1=request.GET.get('email1')
            email2=request.GET.get('email2')
            mobile=request.GET.get('mobile')
            phone=request.GET.get('telephone')
            
            print("email1",email1,"email2",email2,"mobile",mobile,"phone",phone)
            if ticket is None:
                ticket=" "    
            if email1=="":
                email1=None  
            if email2=="":
                email2=None 
            if mobile=="":
                mobile=None  
            if phone=="":
                phone=None                                                                                                            
            if email1 or email2 or mobile or phone:
                print("email1",email1,"email2",email2,"mobile",mobile,"phone",phone)
                Cursor.execute("set nocount on;exec SP_SearchPhoneEmail_PY %s,%s,%s,%s,%s",[mobile,phone,email1,email2,UserId]) # To test exec SP_SearchPhone '4588',21
                search_email_phone=Cursor.fetchone() 
                if search_email_phone:
                    print("--------------------------",search_email_phone,type(search_email_phone))
                if(Cursor.nextset()):
                    search_email_phone1 = Cursor.fetchone() 
                    if search_email_phone1:
                        search_email_phone =search_email_phone1  
                                        
                    print("next data set1datas----------------",search_email_phone)
                # Cursor.nextset()
                # search_email_phone2 = Cursor.fetchone() 
                # print("next data set2----------------",search_email_phone1)
                # if search_email_phone2:
                #     search_email_phone =search_email_phone2
                # Cursor.nextset()
                # search_email_phone3 = Cursor.fetchone() 
                # print("next data set2----------------",search_email_phone1)
                # if search_email_phone3:
                #     search_email_phone =search_email_phone3
                # while (Cursor.nextset()):
                #     search_email_phone = Cursor.fetchone()
                #     print("next data set2----------------",search_email_phone2)
                # if search_email_phone2:
                #     search_email_phone=search_email_phone2
                # while (Cursor.nextset()):
                #     search_email_phone3 = Cursor.fetchone()
                #     print("next data set3----------------",search_email_phone3)
                # if search_email_phone3:
                #     search_email_phone=search_email_phone3
                print("dataaaaaaaaaaaaaa",search_email_phone)
                if(search_email_phone != None):
                    print("Check it is none")
                    get_ticket=search_email_phone[0]
                    print("Get ticket--------------------",get_ticket)
                    ticket=get_ticket
            
            # lead_details,country=selector.get_lead_details(ticket,UserId)
            # activity_log=selector.get_activity_log(ticket)
            # ticket_summary=selector.get_ticket_summary(ticket)
            # lead_score=selector.get_lead_score(ticket)
            # meeting_score=selector.get_meeting_score(ticket)
            # last_comment=selector.get_last_comment(ticket,UserId)
            # sticky_text=selector.get_sticky_text(ticket)
            # print("Last comment--------",last_comment)
            
            # print("Sticky text============================",sticky_text)
            # print("Lead details-------------")
            # if(meetingscore != None):
            #     print("Meeting if")
            #     meetingscore=sum(meetingscore)
            #     meetingscore=(meetingscore/320)*100
                
            # print("Meeting score-----------------------",meeting_score)
            
            # page_data={'ticket':ticket,'country':country,'email_phone':json.dumps(search_email_phone),'lead_details':lead_details,'ticket_summary':ticket_summary,'activity_log':activity_log,'leadscore':lead_score,'meetingscore':meeting_score,'lastcomment':last_comment,'stickytext':sticky_text}
            country_list=selector.get_all_country()
            accountno=selector.get_account_no(ticket)
            seminar_list=selector.get_upcoming_seminar()
            webinars=selector.get_seminar_list(ticket)
            print("Webinar===============================",webinars)
            webinarList=selector.get_webinar_attended(ticket)
            print("Webinar List=========================",webinarList)
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)
    
        return render(request,'sales/LeadProcessing.html',{'ticket':ticket,'country_list':country_list,'accountno':accountno,'seminars':seminar_list,'webinars':webinars,'webinarList': webinarList})
    else:
         return redirect('/login') 
        
   

def logout(request):
    try:
        UserId=request.session['UserId']
        del request.session['UserId']
        print("logout")
        print(UserId)
        selector.user_logout(UserId)
    except:
        print("Exception")
    finally:
        print("cursor close here")
    return redirect('login/')

def pending_tickets(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        dashboard=request.GET.get('spoken')
        print("User idddddddddddddd",dashboard)
        if (dashboard=="spoken"):
             pending_tickets=selector.get_tickets(UserId,"spoken")
        else:
             pending_tickets=selector.get_tickets(UserId,"pending")
        pendingTickets=sorted( pending_tickets,key=lambda tup: tup[1])
        # pendingTickets=[tuple(reversed(t)) for t in pending_tickets]
        # pendingTickets=pending_tickets[::-1]
       
        return render(request,'sales/pendingtickets.html',{'pending_tickets':pendingTickets})
    else:
         return redirect('/login') 

def pending_tckts_load_all(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')   
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        status=request.GET.get('status')
        print("From date-----------------",from_date)
        print("To date------------------",to_date)
        print("Status=============================",status)
        pending_tickets=selector.get_all_tickets(UserId,status,from_date,to_date)
        # paginator = Paginator(load_data, 10)
        print("load data-------------------------",len(pending_tickets))
        return JsonResponse(list(pending_tickets), safe=False)
    else:
         return redirect('/login') 

def resolved_tickets(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        print(UserId)
        
        resolved_tickets=selector.get_tickets(UserId,"resolved")
        
        return render(request,'sales/resolvedtickets.html',{'resolved_tickets':resolved_tickets})
    else:
         return redirect('/login') 

def dormant_ticket(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        print("USer iddddddddddddddddddddd",UserId)
        salesrepId=30
        dormant_tickets=selector.get_tickets(salesrepId,"dormant")        
        return render(request,'sales/dormanttickets.html',{'dormant_tickets':dormant_tickets})
    else:
         return redirect('/login') 



def resolved_tckts_load_all(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        resolved_tickets=selector.get_all_tickets(UserId,"resolved",from_date,to_date)
        # paginator = Paginator(load_data, 10)
        print("load data-------------------------",len(resolved_tickets))
        return JsonResponse(list(resolved_tickets), safe=False)
    else:
        return redirect('/login')

def new_accounts(request):
    active="Live"
    if 'UserId' in request.session:
        change=request.GET.get("change")
        from_date=request.GET.get("from")
        to_date=request.GET.get("to")
        status=request.GET.get("status")
        print("From date====",from_date)
        print("To_date====",to_date)
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
        if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
        else:
                date_yesterday = datetime.today()-timedelta(1)

        date_yesterday=date_yesterday.strftime("%Y-%m-%d")
        if from_date=="":
            from_date=date_yesterday
        if to_date=="":
            to_date=date_today
        
        print("Status----------------------",status)
        if(change):
            accounts_data=selector.get_new_accounts(change,status,from_date,to_date)
            accounts_count=selector.get_new_accounts_count(from_date,to_date)
            print("change is---------------",change)
            
            return HttpResponse(json.dumps({"data":accounts_data,"count":accounts_count}), content_type="application/json")
        else:
           
            
            accounts_data=selector.get_new_accounts("Live","",date_yesterday,date_today)
            accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)
            
            # terminated_data=selector.get_new_accounts("Terminated")
            return render(request,'admin/newAccounts.html',{'accounts_data':accounts_data,'accounts_count':accounts_count,"active":json.dumps(active)})
            # return render(request,'sales/allclients.html',{'accounts_data':accounts_data,'accounts_count':accounts_count,"active":json.dumps(active)})
                
    else:
        return redirect('/login')
#new account variants
def new_accounts_variants(request):
    active="Live"
    if 'UserId' in request.session:
        change=request.GET.get("change")
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
        if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
        else:
                date_yesterday = datetime.today()-timedelta(1)

        date_yesterday=date_yesterday.strftime("%Y-%m-%d")
        
        if (change =="TempApproved" or change=="WaitingApproval"):
            active="pending"
        print("Status----------------------",change)
        
        accounts_data=selector.get_new_accounts_filter(change)
        accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)   
        # accounts_count=selector.get_new_accounts_count_variants(date_yesterday,date_today,change)
        print("Accounts count-----------",accounts_count)
            # terminated_data=selector.get_new_accounts("Terminated")
        return render(request,'admin/newAccounts.html',{'accounts_data':accounts_data,'accounts_count':accounts_count,"active":json.dumps(active)})
                
    else:
        return redirect('/login')

#new account weekly
def new_accounts_variants_weekly(request):
    active="Live"
    if 'UserId' in request.session:
        change=request.GET.get("change")
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
        if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
        else:
                date_yesterday = datetime.today()-timedelta(week_day)

        date_yesterday=date_yesterday.strftime("%Y-%m-%d")
        print("Date yesterday==========",date_yesterday)
        if (change =="TempApproved" or change=="WaitingApproval"):
            active="pending"
        print("Status----------------------",change)
        
        accounts_data=selector.get_new_accounts_weekly_filter(change,date_yesterday,date_today)
        accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)   
        
        print("Accounts count-----------",accounts_count)
            
        return render(request,'admin/newAccounts.html',{'accounts_data':accounts_data,'accounts_count':accounts_count,"active":json.dumps(active)})
                
    else:
        return redirect('/login')
#new accounts click
def new_accounts_click(request):
    active="Live"
    if 'UserId' in request.session:
        
        status=request.GET.get("status")
        if (status =="TempApproved" or status=="WaitingApproval"):
            active="pending"
        fromdate=request.GET.get('fromdate')
        todate=request.GET.get("todate")
        print("Cliked inputs=========================",fromdate,todate,status)
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
        if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
        else:
                date_yesterday = datetime.today()-timedelta(1)

        date_yesterday=date_yesterday.strftime("%Y-%m-%d")
        if fromdate=="":
            fromdate=date_yesterday
        if todate=="":
            todate=date_today
        
        accounts_data=selector.get_new_accounts_click(status,fromdate,todate)
        
        accounts_count=selector.get_new_accounts_count(fromdate,todate)
        
        return HttpResponse(json.dumps({"data":accounts_data,"count":accounts_count}), content_type="application/json")
        # return render(request,'admin/newAccounts.html',{'accounts_data':accounts_data,'accounts_count':accounts_count,"active":json.dumps(active)})
                
    else:
        return redirect('/login')


def sendRemiderMail(request):
    if 'UserId' in request.session:        
        ticket=request.GET.get('ticket')
        subject="Trust Capital - Meeting Reminder"
        sendername=request.session.get('UserName')
        bcc=""
        cc=""
        template="MeetingReminder.html"
        selector.mailSend(ticket,subject,bcc,cc,template,sendername)
        
        return JsonResponse({'success':True})
    else:
        return redirect('/login')

def sendCancelMail(request):
    if 'UserId' in request.session:
        print("Cancel meetingg-----")
        UserId=request.session.get('UserId') 
        ticket=request.GET.get('ticket')
        selector.cancel_meeting_mail(UserId,ticket)
        return JsonResponse({'success':True})
    else:
        return redirect('/login')

def meetingScore(request):
    if 'UserId' in request.session:
        print("Meeting Score")
        
        ticket=request.GET.get('ticket')   
        ticket=ticket.strip()     
        meeting_score=selector.get_meeting_score(ticket)
        print("Meeting score-----",meeting_score)
        return JsonResponse({'score':meeting_score})

    else:
        return redirect('/login')

def manage_meeting(request):
    assess_data=[]
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        ticket=ticket.strip()
        print("Ticket--------------------------",ticket)
       
        # all_meetings=selector.get_all_meeting(ticket)
        all_meetings=selector.get_last_meeting(ticket)
        
        if all_meetings:
            all_meeting=all_meetings[0]
            print("All Meeting",all_meeting)
            assess_data=[
                all_meeting[7],
                all_meeting[8],
                all_meeting[9],
                all_meeting[10],
                all_meeting[11],
                all_meeting[12],
            ]
            print("Assess Data",assess_data)
        print("All meeting----------------",len(all_meetings))
        return render(request,'sales/meeting.html',{'meetings':all_meetings,'assess':assess_data})
    else:
        return redirect('/login')
# def load_meeting_inassessment(request):
#     if 'UserId' in request.session:
#         ticket=request.GET.get('ticket')
#         ticket=ticket.strip()
#         print("Ticket--------------------------",ticket)
       
#         # all_meetings=selector.get_all_meeting(ticket)
#         all_meetings=selector.get_last_meeting(ticket)
#         print("All meeting----------------",len(all_meetings))
#         return JsonResponse({"meetings":all_meetings})
#     else:
#         return JsonResponse({"message":"Session Expired"})


def send_meeting_request(request):

    if 'UserId' in request.session:
        message=""
        bcc="crm@trusttc.com"
        cc=""
        ticket=request.GET.get('ticket')
        flag=int(request.GET.get('flag'))
        sendername=request.session.get('UserName')
        message=service.send_meeting_request(request)
        if message:
            message=message[0]   
        print("Flag--------------------",type(flag))     
        if(flag == 0 or flag == 1):
            subject="Trust Capital – Meeting Confirmation"
            
        if(flag == 2):
            print("Meeting cancelled")
            subject = "Trust Capital – Meeting Cancelled"
            template="MeetingCancelled.html"
            
            selector.mailSend(ticket,subject,bcc,cc,template,sendername)
        print("Subject--------------------------------------",subject)
        if(message == 'PROCEED'):
            print("Proceed---")          
            
            #bcc="aswani.trustlns@gmail.com"
            
            template="MeetingConfirmation.html"
            
            selector.mailSend(ticket,subject,bcc,cc,template,sendername)
            print("Proceed------",message)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')
        
        
# def change_meeting_request(request):
#     if 'UserId' in request.session:
#         ticket=request.GET.get('ticket')
#         flag=1
#         message=service.send_meeting_request(request,flag)
#         message=message[0]
        
#         if(message=='PROCEED'):

            
#             subject="TC Limited – Meeting Confirmation"
#             # bcc="crm@trusttc.com"
#             bcc="aswani.trustlns@gmail.com"
#             cc=" "
#             selector.mailSend(ticket,subject,bcc,cc)
#             print("Proceed------",message)
#         return JsonResponse({"message":message})
#     else:
#         return redirect('/login')

def update_feedback(request):
    if 'UserId' in request.session:
        
        ticket=request.GET.get('ticket')
        message=service.meeting_feedback_update(request)
        print("Message-------------------",message)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')

def update_meetingassessment(request):
    if 'UserId' in request.session:
        print("Meeting assessment update view")
        service.update_meeting_assessment(request)
        message="Meeting assessment updated successfully"
        return JsonResponse({"message":message})
    else:
        return redirect('/login')



def saveMeeting(request):
    if 'UserId' in request.session:
        score=service.save_meeting_score(request)
        ticket=request.GET.get('ticket')
        meeting_score=selector.get_meeting_score(ticket)
        if(meeting_score != None):
            meeting_score=sum(meeting_score)
            meeting_score=(meeting_score/320)*100
        print("Meeting score======",meeting_score)
        return JsonResponse({"score":score,"meetingscore":meeting_score})
    else:
        return redirect('/login')

def liveChatLogs(request):
    if 'UserId' in request.session:
        
        
        ticket=request.GET.get('ticket')
        ticket=ticket.strip()
        print("Ticket--------------------",ticket)        
        chat_logs=selector.get_livechat_logs(ticket)
        print("Chat logs count-------------------",len(chat_logs))
        return JsonResponse({'logs':chat_logs})
    else:
        return redirect('/login')

def emailInbox(request):
    if 'UserId' in request.session:     
        inbox=[]   
        
        page=request.GET.get('page')
        count=request.GET.get('start')
        count_end=request.GET.get('end')
        if(count):
            count=int(count)
        if(count_end):
            count_end=int(count_end)
        inbox_count,inbox_data=selector.get_mail_inbox()
        print("Inbox count==============================",inbox_count)
        if(page is None):                    
            
            inbox=inbox_data[0:20]
            return render(request,'sales/inbox.html',{'count':inbox_count,'mails':inbox_data,'data':json.dumps(inbox_data)})
        else:
            if(page == 'add'):
                inbox=inbox_data[count:count_end]
            if(page=='sub'):
                if(count_end==0 or count_end<0):
                    inbox=inbox_data[0:20]
                else:
                    inbox=inbox_data[count:count_end]
            return JsonResponse({'count':inbox_count,'mails':inbox_data})
        
        
    else:
        return redirect('/login')

def emailRead(request):
    if 'UserId' in request.session:                
        message=request.GET.get('message')        
        message_data,subject,sender,count,multipart=selector.read_mail_inbox(message)
        return render(request,'sales/inboxread.html',{'message':message_data,'subject':subject,'sender':sender,'count':count,'multipart':multipart})
    else:
        return redirect('/login')

def viewDocument(request):
    if 'UserId' in request.session:        
        ticket=request.GET.get('ticket')
        docs=selector.view_document(ticket)
        return JsonResponse({'docs':docs})
    else:
        return redirect('/login')

def viewLoadFunctions(request): # 455325 to test meeting score

    if 'UserId' in request.session:    
        code=0    
        ticket=request.GET.get('ticket')
        
        ticket=ticket.strip()
        UserId=request.session.get('UserId')
        activity_log=selector.get_activities_log(ticket)
        lead_details=selector.get_lead_details(ticket,UserId)
        if lead_details:
            cid=lead_details[10]
            code=selector.get_code_country(cid)
        country_list=selector.get_all_country()    
        leadscore=selector.get_lead_score(ticket)
        last_comment=selector.get_last_comment(ticket,UserId)
        accountno=selector.get_account_no(ticket)
        ticket_summary=selector.get_ticket_summary(ticket)
        sticky_text=selector.get_sticky_text(ticket)
        # webinarList=selector.get_seminar_list(ticket)
        webinarList=selector.get_webinar_attended(ticket)
        reminders=selector.load_ticket_reminders(UserId,ticket)
        print("Rminders=====================================",reminders)
        # email=request.session.get("Email")
        # send_items=selector.template_send_items_list(email)
        print("Last comment--------",last_comment)
        meetingscore=selector.get_meeting_score(ticket)
      
        print("Meetin score=============================",meetingscore)
        if(meetingscore != None):
            meetingscore=sum(meetingscore)
            meetingscore=(meetingscore/320)*100
            
        print("Meeting score----",meetingscore)
        print("Sticky text========",sticky_text)
        print("End---------------------")
        return JsonResponse({'leads':lead_details,'activities':activity_log,'country_list':country_list,'ticket_summary':ticket_summary,'leadscore':leadscore,'meetingscore':meetingscore,'lastcomment':last_comment,'stickytext':sticky_text,'accountno':accountno,'webinarList':webinarList,'code':code,'reminders':reminders})
    else:
        return JsonResponse({"message":"Your session expired! Please login to continue"})
def activity_log(request):
    if 'UserId' in request.session:        
        ticket=request.GET.get('ticket')
        activity_log=selector.get_activities_log(ticket)
        return JsonResponse({'activities':activity_log})
    else:
        return redirect('/login')


def assign_rep(request):
    if 'UserId' in request.session:
        assign=service.assign_salesRep(request)
        print("Assign-------",assign)
        return JsonResponse({'assign':assign})
    else:
        return redirect('/login')

def name_search(request):
    if 'UserId' in request.session:
        searched_name=request.GET.get('name')
        UserId=request.session.get('UserId')
        name_list=selector.get_name_search(searched_name,UserId)
        return JsonResponse({'name_list':name_list})
     
    else:
        return redirect('/login')

def phone_search(request):
    if 'UserId' in request.session:
        searched_name=request.GET.get('phone')
        UserId=request.session.get('UserId')
        phone_list=selector.get_phone_search(searched_name,UserId)
        return JsonResponse({'phone_list':phone_list})
     
    else:
        return redirect('/login')


def mail_search(request):
    if 'UserId' in request.session:
        searched_name=request.GET.get('mail')
        UserId=request.session.get('UserId')
        mail_list=selector.get_mail_search(searched_name,UserId)
        return JsonResponse({'mail_list':mail_list})
     
    else:
        return redirect('/login')

#Account status update

def account_status(request):
    if 'UserId' in request.session:
        
        accountNo=request.POST.get('formaccountno')
        ticket=request.POST.get('formticket')
        print("Account number=============================",accountNo)
        msg=selector.account_status_check_update(accountNo,ticket,request)
        return JsonResponse({"msg":msg})
    else:
        return redirect('/login')

#Ticket status update
def ticket_status(request):
    if 'UserId' in request.session:
        ticket=request.POST.get('formticket')
        print("Ticket-------",ticket)
        msg="Ticket updated Successfully"
        selector.ticket_validity_check_update(ticket,request)
        return JsonResponse({"msg":msg})
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
        print("Template selectio=====")
        selector.email_template_selection(lang,sub,fromaddr,to,title,name,userid,ticket)
        return JsonResponse({"success":"Email Send"})
    else:
        return JsonResponse({"success":"Your session expired! Please login to continue"})

#Manage ticket Email send

def email_send(request):
    if 'UserId' in request.session:   
        # fromaddr=request.POST.get('from')
        to=request.POST.get('to')
        name=request.POST.get('name')
        title=request.POST.get('tit')
        sub=request.POST.get('subject')
        emailbody=request.POST.get('body')
        selector.email_compose(to,sub,emailbody)
        return JsonResponse({"success":True})
    else:
        return redirect('/login')

def save_reminder_details(request):
    if 'UserId' in request.session:
        print("Save reminder view=========")
        userid=request.session.get('UserId')
        mail=request.session.get('Email')
        date=request.POST.get('date')
        time=request.POST.get('time')
        ticket=request.POST.get('ticket')
        subject=request.POST.get('subject')
        login=request.POST.get('login')
        color=request.POST.get('color')
        flag=int(request.POST.get('flag'))
        # if(subject==None):
        #     subject=" "
        print("Flag=====================================",type(flag))
        print("User id=====================================",type(userid))
        print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",type(date),type(time),type(color),type(login))
        selector.save_reminder(userid,ticket,subject,date,time,login,color,mail,flag)
        reminders=selector.load_ticket_reminders(userid,ticket)
        return JsonResponse({"success":True,"reminders":reminders})
    else:
        return redirect('/login')
#save insert ticket logs
def ticket_logs_insertion(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        ticket=request.GET.get('ticket')
        logdata=request.GET.get('logdata')
        logtype=request.GET.get('logtype')
        print("Chat test============",userid,ticket,logdata,logtype)
        selector.insert_ticket_logs(userid,logdata,logtype,ticket)
        return JsonResponse({"success":True})
    else:
        return redirect('/login')

def update_sticky_notes(request):
    if 'UserId' in request.session:
        print("Sticky update======================")
        userid=request.session.get('UserId')
        notes=request.GET.get('note')
        update=selector.save_Sticky_text(notes,userid)
        return JsonResponse({"success":True})
    else:
        return redirect('/login')
def resolve_tickets(request):
    if 'UserId' in request.session:
        
        userid=request.session.get('UserId')
        ticket=request.GET.get('ticket')
        reason=request.GET.get('reason')
        print("Reason======================",reason)
        msg=selector.resolve_ticket(ticket,userid,reason)
        
        return JsonResponse({"message":msg})
    else:
        return redirect('/login')
#List upcoming seminars
def upcomingSeminars(request):  
    if 'UserId' in request.session:        
        ticket=request.GET.get('ticket') 
        print("Upcoming seminar ticket======",ticket)
        seminar_list=selector.get_upcoming_seminar()
        webinars=selector.get_seminar_list(ticket)
        print("Seminar List======================",seminar_list)
        print("Seminar List======================",webinars)
        return JsonResponse({"seminars":seminar_list,"webinars":webinars})
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
        message=selector.register_seminar(title,name,to_addr,seminartitle,ticket,userid)
                                           
        return JsonResponse({"msg":message})
    else:
       return JsonResponse({"msg":"Your session expired! Please login to continue"}) 
#Update seminar
def updateseminar(request):
    if 'UserId' in request.session:
        
        userid=request.session.get('UserId')
        status=request.GET.get('status')
        seminar=request.GET.get('seminar')       
        ticket=request.GET.get('ticket')
        print("Status---------------------",ticket,status,seminar,userid)
        selector.update_seminar_status(ticket,status,seminar,userid)
        return JsonResponse({"msg":"Updated successfully"})
    else:
        return JsonResponse({"msg":"Your session expired! Please login to continue"})
#List all seminar
def list_all_seminar(request):
    if 'UserId' in request.session:        
              
        ticket=request.GET.get('ticket')
        selector.get_seminar_list(ticket)
        return JsonResponse({"msg":"List all seminars"})
    else:
        return redirect('/login') 
#Open demo account
def open_demoaccount(request):
    if 'UserId' in request.session:
        title=request.GET.get('title')
        name=request.GET.get('name')
        email=request.GET.get('email')
        phone=request.GET.get('phone')
        country=int(request.GET.get('country'))
        print("All open demo data====",title,name,email,phone,country)
        selector.open_demo_account(title,name,email,phone,country)
        return JsonResponse({"msg":"Demo account opened"})
    else:
        return JsonResponse({"msg":"Your session expired! Please login to continue"})
#Email template send items
def send_items_list(request):
    if 'UserId' in request.session: 
        email=request.GET.get("mail")
        print("Leads mail Id===============",email)
        count,itemsList=selector.template_send_items_list(email)
      
        return JsonResponse({"count":count,"send":itemsList})
def email_data(request):
    if 'UserId' in request.session:
        return render(request,'test/index.html')

#Read send itms mail

def read_send_items(request):

    if 'UserId' in request.session: 
        print("Read send items=============")
        email=request.GET.get("mail")
        msg_id=request.GET.get('message')
        message_data,subject,sender,multipart=selector.read_mail_senditems(email,msg_id)
        return JsonResponse({"message":message_data,"subject":subject,"multipart":multipart})
#Sales Report
def get_sales_report(request):
    if 'UserId' in request.session:        
        userid=request.session.get('UserId')  
        
        salesrep=selector.get_salesrep_permission(userid)
        
        return render(request,'sales/salesreport.html',{'salesrep':salesrep})
    else:
        return redirect('/login')
#Sales Report with date
def get_sales_report_date(request):
    if 'UserId' in request.session:        
        
        repId=request.GET.get('repId')
        from_date=request.GET.get('from_date')
        to_date=request.GET.get('to_date')
        print("From date=======================",from_date,to_date,repId)
        salesreport,interested=selector.get_sales_call_report(from_date,to_date,repId)
        print("Report=====",salesreport)
        return JsonResponse({"report":salesreport,"interested":interested})
    else:
        return redirect('/login')
#Monthly sales report
def get_sales_report_monthly(request):
    if 'UserId' in request.session:        
       
        repId=request.GET.get('repId')
        month=request.GET.get('month')
        year=request.GET.get('year')
        print("From date=======================",month,year,repId)
        salesreport=selector.get_sales_call_report_monthly(month,year,repId)
        print("Report=====",salesreport)
        return JsonResponse({"report":salesreport})
    else:
        return redirect('/login')
#print Sales call Report
def print_sales_call_report(request):
    if 'UserId' in request.session: 
        repId=request.GET.get('SalesRep')
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        print("From date=======================",from_date,to_date,repId)
        salesreport,interested=selector.get_sales_call_report(from_date,to_date,repId)
        if salesreport:
            total_row=salesreport[-1]
            spoken=total_row[1]
            total=total_row[6]
            spokenper=round((spoken/total)*100,2)
        print("Last from th tuple====",total_row,spoken,total,spokenper)
        return render(request,'sales/SalesreportPrint.html',{"reports":salesreport,"interested":interested,"repname":repId,"from":from_date,"to":to_date,"spoken":spokenper})
    else:
        return redirect('/login')

#Live chat Page render

def live_chat(request):
    if 'UserId' in request.session:
        return render(request,'sales/livechat.html')
    else:
        return redirect('/login')
def show_calendar(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
       
        print("Reminders========")
        return render(request,'sales/calendar.html')
    else:
        return redirect('/login')
def show_events(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        reminders=selector.get_all_calender_events(userid)
        return JsonResponse({"events":reminders})
    else:
        return redirect('/login')












    












   