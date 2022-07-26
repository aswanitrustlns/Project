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
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from .models import TblClients,TblEwalletTransaction,TblSaleslead,TblActionreasons,TblUser
from django.apps import apps
from gtts import gTTS
import os
import json
from .dashboard_selectors import DashboardSelector
from .services import Services
from .selectors import Selector
from django.core.serializers import serialize
from .serializers import ClentsSerializer
from .emailservices import EmailServices

insta_username = "Tc_limited"
insta_password = "T@Cmited21!!"
all_data={}

# Load_Insta=instaloader.Instaloader()
Cursor=connection.cursor()
selector=Selector()
service=Services()
sales_dash=DashboardSelector()
emailservice=EmailServices()
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
    
    model=apps.get_model('CRF','TblUser')
    msg="Username and Password do not match"
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        server_name=request.POST.get('servername')
        
    try:  
        userInfo=model.objects.using('crf').filter(username=username).first()
        # crfUserId=userInfo.userid
        if(userInfo!=None):
            request.session['crf']="crfuser"
        else:
            request.session['crf']="notuser"
      
        
        UserId=selector.get_loged_user_info(username)  
        
        request.session['UserId'] = UserId
        request.session['UserLogin'] = username
        if UserId==21:
            
            adminrole="admin" 
            request.session['role']="manager"
        if UserId==28:
            
            adminrole="backoffice" 
            request.session['role']="backoffice"
        # if UserId==56:
        #     adminrole="complaints"
        #     request.session['role']="complaints"
        else:
            adminrole="sales" 
            request.session['role']="salesrep"
        # request.session['UserId'] = 30
        connect=selector.dll_connection(username,server_name,password)
        
    except Exception as e:
        print("Exception------------",e.__class__)
        connect=1
        msg="User not Found"
        request.session["message"]=msg        
   
    
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
        unassign=""
        UserId=request.session.get('UserId')
        selrep=request.GET.get('repId')
        if(selrep!=None):
            UserId=selrep
        # else:
        #     UserId=request.session.get('UserId')
       
        
       
        permission_check=selector.user_role_selection(UserId)    
        backoffice=permission_check[5]
        manager=permission_check[11]
        salesRep=permission_check[22]
        complaints=permission_check[14]
        viewunassigned=permission_check[25]
        seminarconf=permission_check[23]
        if seminarconf:
            request.session['seminarconf']="True"
        else:
            request.session['seminarconf']="False"

        if complaints:
            request.session['compliance']="True"
        if viewunassigned:
            unassign="True"
            request.session['unassign']="True"
        else:
           request.session['unassign']="False" 
        
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
        
        if manager:
                          
             request.session['role']="manager"
             
            #  dashbord_data=sales_dash.admin_dashboard(UserId)  
             dashbord_data=sales_dash.manager_dashboard(UserId)    
             
            #  return render(request,'sales/dashboard.html',dashbord_data)
             return render(request,'sales/managerdashboard.html',dashbord_data)
        if salesRep:
            
            request.session['role']="salesrep" 
            dashbord_data=sales_dash.sales_dashboard(UserId)     
            
            return render(request,'sales/dashboard.html',dashbord_data)
        if backoffice:
            request.session['role']="backoffice"
            dashbord_data=sales_dash.backoffice_dashboard(UserId)    
            
            #  return render(request,'sales/dashboard.html',dashbord_data)
            return render(request,"backoffice/dashboard.html",dashbord_data)

        if complaints:
            request.session['role']="complaints"
            dashbord_data=sales_dash.complaint_dashboard(UserId)
            return render(request,"compliance/dashboard.html",dashbord_data)

    else:
         return redirect('/login') 


   
def lead(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        lead="lead"
        leads_data,leads_count,fromdate,todate=selector.get_leads(lead,from_date,to_date)
        
        # print("Leads data---------------------",leads_data)
        return render(request,'sales/Leads.html',{'leads_data':leads_data,'leads_count':leads_count,'from':fromdate,'to':todate})
    else:
         return redirect('/login') 

def lead_load_all(request): 
    
    lead="all"
    from_date=request.GET.get('from')
    to_date=request.GET.get('to')
    load_data,leads_count,fromdate,todate=selector.get_leads(lead,from_date,to_date)   
    return JsonResponse(load_data, safe=False)

def lead_load_click(request): 
    
    status=request.GET.get('status')  
    count=request.GET.get('count')
    if count:
        count=int(count)
    leads_data=selector.get_leads_clicks(status,count)  
    return JsonResponse(leads_data, safe=False)
   

# def new_accounts(request):
#     if 'UserId' in request.session:
#         new_accounts_data=selector.get_new_accounts()
#         print("New Accounts page data")
#         # return render(request,'admin/newaccounts.html',{'page_data':new_accounts_data})
#     else:
#          return redirect('/login')

def lead_duplicate_check(request):
    
    phone=request.GET.get('phone')
    email=request.GET.get('email')
    print("Phone,email====",phone,email)
    duplicate=selector.check_duplicate(phone,email)
    print("Duplicate=====",duplicate)
    if duplicate:
        return JsonResponse({"success":True,"duplicate":duplicate})
    else:
        return JsonResponse({"success":False})

def view_merge(request):
    
    demoid=request.GET.get('demoid')
    ticket=request.GET.get('ticket')
    email1=request.GET.get('email1')
    email2=request.GET.get('email2')
    mobile=request.GET.get('mobile')
    telephone=request.GET.get('telephone') 
    selector.merge_ticket(ticket,email1,email2,mobile,telephone) 
    selector.close_lead(demoid,ticket)
    return JsonResponse({'success':True})

def create_ticket(request):
    
    email,phone,ticket=service.create_ticket_service(request)
    return JsonResponse({"success":True,"email":email,"phone":phone,"ticket":ticket})    

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
            if hash_check>=0:    
                selector.merge_ticket(ticket,email1,email2,mobile,telephone)                
                
            login=0   
            user_permission=selector.user_permission_check(UserId,ticket,login)
            user_permission=user_permission[0]                  
            if user_permission:
                return JsonResponse({'success':True,'ticket':ticket})
            else:
                return JsonResponse({'success':False,'ticket':ticket})
        except:
            print("Error")
    else:
             return render(request,'admin/LeadProcessing.html')
            
       
        
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
            id=request.GET.get('id')
            print("email1",email1,"email2",email2,"mobile",mobile,"phone",phone,ticket,id)
            if ticket is None:
                email,phone,ticket=service.create_ticket_service(request)
                print("created ticket===",ticket)
            # if email1=="":
            #     email1=None  
            # if email2=="":
            #     email2=None 
            # if mobile=="":
            #     mobile=None  
            # if phone=="":
            #     phone=None                                                                                                            
            # if email1 or email2 or mobile or phone:
                
            #     Cursor.execute("set nocount on;exec SP_SearchPhoneEmail_PY %s,%s,%s,%s,%s",[mobile,phone,email1,email2,UserId]) # To test exec SP_SearchPhone '4588',21
            #     search_email_phone=Cursor.fetchone() 
            #     if search_email_phone:
            #         print("--------------------------",search_email_phone,type(search_email_phone))
            #     if(Cursor.nextset()):
            #         search_email_phone1 = Cursor.fetchone() 
            #         if search_email_phone1:
            #             search_email_phone =search_email_phone1  
            #     if(search_email_phone != None):
            #         get_ticket=search_email_phone[0]
            #         ticket=get_ticket
            
            
            country_list=selector.get_all_country()
            accountno=selector.get_account_no(ticket)
            seminar_list=selector.get_upcoming_seminar()
            webinars=selector.get_seminar_list(ticket)
            webinarList=selector.get_webinar_attended(ticket)
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
        if (dashboard=="spoken"):
             pending_tickets,fromdate,todate=selector.get_tickets(UserId,"spoken")
        else:
             pending_tickets,fromdate,todate=selector.get_tickets(UserId,"pending")
        sourcelist=selector.get_sources()
        salesrep=selector.get_salesrep_permission(UserId)
        pendingTickets=sorted( pending_tickets,key=lambda tup: tup[1])
        # pendingTickets=[tuple(reversed(t)) for t in pending_tickets]
        # pendingTickets=pending_tickets[::-1]
       
        return render(request,'sales/pendingtickets.html',{'pending_tickets':pendingTickets,'status':json.dumps("Pending"),'from':fromdate,'to':todate,'sources':sourcelist,'salesrep':salesrep})
    else:
         return redirect('/login') 
def pending_tickets_from_summary(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        summary=request.GET.get('summary')
        status=request.GET.get('status')
        pending_tickets,fromdate,todate=selector.get_tickets_summary(UserId,summary,status)
        return render(request,'sales/pendingtickets.html',{'pending_tickets':pending_tickets,'status':json.dumps(status),'from':json.dumps(fromdate),'to':json.dumps(todate)})
    else:
         return redirect('/login')

def pending_tckts_load_all(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')   
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        status=request.GET.get('status')
        repId=request.GET.get('repId')
        source=request.GET.get('source')
        
        pending_tickets,fromdate,todate=selector.get_all_tickets(UserId,status,from_date,to_date,repId,source)

        # return JsonResponse(list(pending_tickets), safe=False)
        return HttpResponse(json.dumps({"data":pending_tickets,"from":fromdate,"to":todate}), content_type="application/json")
    else:
         return redirect('/login') 

def resolved_tickets(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        resolved_tickets,fromdate,todate=selector.get_tickets(UserId,"resolved")
        return render(request,'sales/resolvedtickets.html',{'resolved_tickets':resolved_tickets,'from':fromdate,'to':todate})
    else:
         return redirect('/login') 

def dormant_ticket(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        # salesrepId=30
        dormant_tickets,fromdate,todate=selector.get_tickets(UserId,"dormant")        
        return render(request,'sales/dormanttickets.html',{'dormant_tickets':dormant_tickets})
    else:
         return redirect('/login') 



def resolved_tckts_load_all(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        resolved_tickets,fromdate,todate=selector.get_all_tickets(UserId,"resolved",from_date,to_date)
        return HttpResponse(json.dumps({"data":resolved_tickets,"from":fromdate,"to":todate}), content_type="application/json")
        
    else:
        return redirect('/login')

def new_accounts_pend(request):
    active="Live"
    if 'UserId' in request.session:
        role=request.session.get("role")
        
        change=request.GET.get("change")
        from_date=request.GET.get("from")
        to_date=request.GET.get("to")
        status=request.GET.get("status")
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
        
        
        if(change):
            if status=="Live":
                status="FundedLive"
            if status=="Pending":
                status="TempApprovedPending"
            
            accounts_data=selector.get_new_accounts(change,status,from_date,to_date)
            accounts_count=selector.get_new_accounts_count(from_date,to_date)
            print("change is---------------",change)
            
            return HttpResponse(json.dumps({"data":accounts_data,"count":accounts_count,'from':from_date,'to':to_date}), content_type="application/json")
                
    else:
        return redirect('/login')
#new account variants
def new_accounts_variants(request):
    active="Live"
    if 'UserId' in request.session:
        try:
            Cursor=connection.cursor()
            role=request.session.get("role")
            change=request.GET.get("change")
            if(change=="" or change==None):
                change="NonFunded"
            status=request.GET.get("status")
            fromd=request.GET.get("fromd")
            tod=request.GET.get("tod")
            print("status from first===",status)
            if(status=="" or status==None):
                status="Live"

            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                    date_yesterday = datetime.today()-timedelta(3)
            else:
                    date_yesterday = datetime.today()-timedelta(1)
            #date_yesterday = "1900-01-01"
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            if(fromd!=None and fromd!=""):
                date_yesterday=fromd
            if(tod!=None and tod!=""):
                date_today=tod

            if (change =="TempApproved" or change=="WaitingApproval"):
                active="pending"
            accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)  
            print("Statues==========",active)
            if(status=="Pending" or status=="pending"):
                print("Pending status====",status)
                active="pending"
                if(change=="TempApproved"):
                    accounts_data=selector.get_new_accounts_click("TempApprovedPending",date_yesterday,date_today)#get_new_accounts_filter
                else:
                    if(change=="WaitingApproval"):
                        accounts_data=selector.get_new_accounts_click("WaitingApprovalPending",date_yesterday,date_today)#get_new_accounts_filter
                    else:
                        accounts_data=selector.get_new_accounts_click("WaitingApprovalPending",date_yesterday,date_today)#get_new_accounts_filter
            
            if(status=="Rejected"):
                active="Rejected"
                if(change=="TempApproved"):
                    accounts_data=selector.get_new_accounts_click("TempApprovedRejected",date_yesterday,date_today)#get_new_accounts_filter
                else:
                    if(change=="WaitingApproval"):
                        accounts_data=selector.get_new_accounts_click("WaitingApprovalRejected",date_yesterday,date_today)#get_new_accounts_filter
                    else:
                        accounts_data=selector.get_new_accounts_click("WaitingApprovalRejected",date_yesterday,date_today)#get_new_accounts_filter
                return HttpResponse(json.dumps({"data":accounts_data,"count":accounts_count,'from':date_yesterday,'to':date_today},default=str), content_type="application/json")
            if(status=="Live"):
                active="Live"
                if(change=="Funded"):
                    accounts_data=selector.get_new_accounts_click("FundedLive",date_yesterday,date_today)#get_new_accounts_filter
                else:
                    if(change=="NonFunded"):
                        accounts_data=selector.get_new_accounts_click("NonFundedLive",date_yesterday,date_today)#get_new_accounts_filter
                    else:
                        accounts_data=selector.get_new_accounts_click("NonFundedLive",date_yesterday,date_today)#get_new_accounts_filter
            if(status=="Closed"):
                active="Closed"
                if(change=="Funded"):
                    accounts_data=selector.get_new_accounts_click("FundedClosed",date_yesterday,date_today)#get_new_accounts_filter
                else:
                    if(change=="NonFunded"):
                        accounts_data=selector.get_new_accounts_click("NonFundedClosed",date_yesterday,date_today)#get_new_accounts_filter
                    else:
                        accounts_data=selector.get_new_accounts_click("NonFundedClosed",date_yesterday,date_today)#get_new_accounts_filter
                return HttpResponse(json.dumps({"data":accounts_data,"count":accounts_count,'from':date_yesterday,'to':date_today},default=str), content_type="application/json")
            if(status=="Terminated"):
                active="Exist"
                if(change=="Funded"):

                    accounts_data=selector.get_new_accounts_click("FundedTerminated",date_yesterday,date_today)#get_new_accounts_filter
                else:
                    if(change=="NonFunded"):
                        accounts_data=selector.get_new_accounts_click("NonFundedTerminated",date_yesterday,date_today)#get_new_accounts_filter
                    else:
                        accounts_data=selector.get_new_accounts_click("NonFundedTerminated",date_yesterday,date_today)#get_new_accounts_filter

            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"FundedLive"])
            live_funded_today=Cursor.fetchone()
            if live_funded_today:
                live_funded_today=live_funded_today[0]
            
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"NonFundedLive"])
            live_nonfund=Cursor.fetchone()
            if live_nonfund:
                live_nonfund=live_nonfund[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"TempApprovedPending"])
            pending_approved=Cursor.fetchone()
            if pending_approved:
                pending_approved=pending_approved[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"WaitingApprovalPending"])
            pending_waiting=Cursor.fetchone()
            if pending_waiting:
                pending_waiting=pending_waiting[0]
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()   
        return render(request,'sales/newAccounts.html',{'account_data':accounts_data,'from':date_yesterday,'to':date_today,'fundcount':live_funded_today,'nonfundcount':live_nonfund,'approved':pending_approved,'waiting':pending_waiting,"active":json.dumps(active),'role':json.dumps(role)})
                
    else:
        return redirect('/login')

#new account weekly
def new_accounts_variants_weekly(request):
    active="Live"
    if 'UserId' in request.session:
        try:
            Cursor=connection.cursor()
            role=request.session.get("role")
            change=request.GET.get("change")
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                    date_yesterday = datetime.today()-timedelta(3)
            else:
                    date_yesterday = datetime.today()-timedelta(week_day)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            if (change =="TempApproved"):
                active="pending"
                accounts_data=selector.get_new_accounts_click("TempApprovedPending",date_yesterday,date_today)
            if(change=="WaitingApproval"):
                active="pending"
                accounts_data=selector.get_new_accounts_click("WaitingApprovalPending",date_yesterday,date_today)
            if(change=="NonFunded"):
                accounts_data=selector.get_new_accounts_click("NonFundedLive",date_yesterday,date_today)
            if(change=="Funded"):
                accounts_data=selector.get_new_accounts_click("FundedLive",date_yesterday,date_today)
            # accounts_data=selector.get_new_accounts_weekly_filter(change,date_yesterday,date_today)
            # accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)   
            # print("Accounts count====",accounts_count)
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"FundedLive"])
            live_funded_today=Cursor.fetchone()
            if live_funded_today:
                live_funded_today=live_funded_today[0]
            
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"NonFundedLive"])
            live_nonfund=Cursor.fetchone()
            if live_nonfund:
                live_nonfund=live_nonfund[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"TempApprovedPending"])
            pending_approved=Cursor.fetchone()
            if pending_approved:
                pending_approved=pending_approved[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"WaitingApprovalPending"])
            pending_waiting=Cursor.fetchone()
            if pending_waiting:
                pending_waiting=pending_waiting[0]
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return render(request,'sales/newAccounts.html',{'account_data':accounts_data,'from':date_yesterday,'to':date_today,'fundcount':live_funded_today,'nonfundcount':live_nonfund,'approved':pending_approved,'waiting':pending_waiting,"active":json.dumps(active),'role':json.dumps(role)})
                
    else:
        return redirect('/login')
        
#new accounts click
def new_accounts_click(request):
    active="Live"
    if 'UserId' in request.session:
        
        status=request.GET.get("status")
        if (status =="TempApproved"):
        
            active="pending"
            status="TempApprovedPending"

        if (status=="WaitingApproval"):
            active="pending"
            status="WaitingApprovalPending"

        fromdate=request.GET.get('fromdate')
        todate=request.GET.get("todate")
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
        print("Accounts data===",accounts_data)
        return HttpResponse(json.dumps({"data":accounts_data,"count":accounts_count,'from':fromdate,'to':todate},default=str), content_type="application/json")
        
                
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
        UserId=request.session.get('UserId') 
        ticket=request.GET.get('ticket')
        selector.cancel_meeting_mail(UserId,ticket)
        return JsonResponse({'success':True})
    else:
        return redirect('/login')

def meetingScore(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')   
        ticket=ticket.strip()     
        meeting_score=selector.get_meeting_score(ticket)
        return JsonResponse({'score':meeting_score})

    else:
        return redirect('/login')

def manage_meeting(request):
    assess_data=[]
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        ticket=ticket.strip()
        all_meetings=selector.get_last_meeting(ticket)
        
        if all_meetings:
            all_meeting=all_meetings[0]
            assess_data=[
                all_meeting[7],
                all_meeting[8],
                all_meeting[9],
                all_meeting[10],
                all_meeting[11],
                all_meeting[12],
            ]
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
         
        if(flag == 0 or flag == 1):
            subject="Trust Capital – Meeting Confirmation"
            
        if(flag == 2):
            
            subject = "Trust Capital – Meeting Cancelled"
            template="MeetingCancelled.html"
            
            selector.mailSend(ticket,subject,bcc,cc,template,sendername)
        
        if(message == 'PROCEED'):
            
            template="MeetingConfirmation.html"
            
            selector.mailSend(ticket,subject,bcc,cc,template,sendername)
            
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
        return JsonResponse({"message":message})
    else:
        return redirect('/login')


def update_meetingassessment(request):
    if 'UserId' in request.session:
        
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
        
        return JsonResponse({"score":score,"meetingscore":meeting_score})
    else:
        return redirect('/login')

def liveChatLogs(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        ticket=ticket.strip()
        chat_logs=selector.get_livechat_logs(ticket)
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
            if lead_details[0]!=0:
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
        # email=request.session.get("Email")
        # send_items=selector.template_send_items_list(email)
        
        meetingscore=selector.get_meeting_score(ticket)
        if(meetingscore != None):
            meetingscore=sum(meetingscore)
            meetingscore=(meetingscore/320)*100
       
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
        msg=selector.account_status_check_update(accountNo,ticket,request)
        return JsonResponse({"msg":msg})
    else:
        return redirect('/login')

#Ticket status update
def ticket_status(request):
    if 'UserId' in request.session:
        ticket=request.POST.get('formticket')
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
        userid=request.session.get('UserId')
        mail=request.session.get('Email')
        date=request.POST.get('date')
        time=request.POST.get('time')
        ticket=request.POST.get('ticket')
        subject=request.POST.get('subject')
        login=request.POST.get('login')
        color=request.POST.get('color')
        flag=int(request.POST.get('flag'))
        selector.save_reminder(userid,ticket,subject,date,time,login,color,mail,flag)
        reminders=selector.load_ticket_reminders(userid,ticket)
        return JsonResponse({"success":True,"reminders":reminders})
    else:
        return redirect('/login')
#save insert ticket logs
def ticket_logs_insertion(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=request.session.get('UserId')
        ticket=request.GET.get('ticket')
        logdata=request.GET.get('logdata')
        logtype=request.GET.get('logtype')
        
        today=datetime.today()
        reasondata_exist=TblActionreasons.objects.filter(ticket=ticket).exists()
        if(reasondata_exist):
            reasondata=TblActionreasons.objects.get(ticket=ticket)
            duedate=reasondata.duedate
            print("Due date=====",duedate)
            if(duedate.timestamp() > today.timestamp()):
                message="Please try after "+str(duedate)
                print("Please try after due date====")
            else:
                reasondata.reason=logdata
                reasondata.updated=today
                reasondata.save()
                message="Your request approved"
        selector.insert_ticket_logs(userid,logdata,logtype,ticket)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')

def update_sticky_notes(request):
    if 'UserId' in request.session:
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
        msg=selector.resolve_ticket(ticket,userid,reason)
        
        return JsonResponse({"message":msg})
    else:
        return redirect('/login')
#List upcoming seminars
def upcomingSeminars(request):  
    if 'UserId' in request.session:        
        ticket=request.GET.get('ticket') 
        seminar_list=selector.get_upcoming_seminar()
        webinars=selector.get_seminar_list(ticket)
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
#Missed Live chat 
def missed_live_chat(request):
    if 'UserId' in request.session:  
        missedchat=selector.get_missedchat()
        print("Missed chat",missedchat)
        return render(request,'sales/missedchats.html',{"missed":missedchat})
    else:
        return redirect('/login') 

#Open demo account
def open_demoaccount(request):
    if 'UserId' in request.session:
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        title=request.GET.get('title')
        name=request.GET.get('name')
        email=request.GET.get('email')
        phone=request.GET.get('phone')
        country=int(request.GET.get('country'))
        selector.open_demo_account(user,server,password,title,name,email,phone,country)
        return JsonResponse({"msg":"Demo account opened"})
    else:
        return JsonResponse({"msg":"Your session expired! Please login to continue"})

#Email template send items
def send_items_list(request):
    if 'UserId' in request.session: 
        email=request.GET.get("mail")
        count,itemsList=selector.template_send_items_list(email)
      
        return JsonResponse({"count":count,"send":itemsList})
# def email_data(request):
#     if 'UserId' in request.session:
#         return render(request,'test/index.html')
#Email template send items backoffice
def send_items_list_backoffice(request):
    if 'UserId' in request.session: 
        email=request.GET.get("mail")
        count,itemsList=selector.template_send_items_backoffice_list(email)
        return JsonResponse({"count":count,"send":itemsList})
#Email template send items sales
def send_items_list_sales(request):
    if 'UserId' in request.session: 
        email=request.GET.get("mail")
        count,itemsList=selector.template_send_items_sales_list(email)
        return JsonResponse({"count":count,"send":itemsList})
#Email template send items sales
def send_items_list_support(request):
    if 'UserId' in request.session: 
        email=request.GET.get("mail")
        count,itemsList=selector.template_send_items_support_list(email)
        return JsonResponse({"count":count,"send":itemsList})
def email_data(request):
    if 'UserId' in request.session:
        return render(request,'test/index.html')

#Read send itms mail
def read_send_items(request):

    if 'UserId' in request.session: 
        username="crm@trusttc.com"
        app_password="Vydw&663"
        email=request.GET.get("mail")
        msg_id=request.GET.get('message')
        message_data,subject,sender,multipart=selector.read_mail_senditems(email,msg_id,username,app_password)
        return JsonResponse({"message":message_data,"subject":subject,"multipart":multipart})

#Read send itms backoffice mail
def read_backoffice_send_items(request):

    if 'UserId' in request.session: 
        username="backoffice@trusttc.com"
        app_password="iyP4a9?9"
        email=request.GET.get("mail")
        msg_id=request.GET.get('message')
        message_data,subject,sender,multipart=selector.read_mail_senditems(email,msg_id,username,app_password)
        return JsonResponse({"message":message_data,"subject":subject,"multipart":multipart})

#Read send itms sales mail
def read_sales_send_items(request):

    if 'UserId' in request.session: 
        username="sales@trusttc.com"
        app_password="otBa62~1"
        email=request.GET.get("mail")
        msg_id=request.GET.get('message')
        message_data,subject,sender,multipart=selector.read_mail_senditems(email,msg_id,username,app_password)
        return JsonResponse({"message":message_data,"subject":subject,"multipart":multipart})

#Read send itms sales mail
def read_support_send_items(request):

    if 'UserId' in request.session: 
        username="support@trusttc.com"
        app_password="yA8g3m9&"
        email=request.GET.get("mail")
        msg_id=request.GET.get('message')
        message_data,subject,sender,multipart=selector.read_mail_senditems(email,msg_id,username,app_password)
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
        salesreport,interested=selector.get_sales_call_report(from_date,to_date,repId)
        return JsonResponse({"report":salesreport,"interested":interested})
    else:
        return redirect('/login')
#Monthly sales report
def get_sales_report_monthly(request):
    if 'UserId' in request.session:        
       
        repId=request.GET.get('repId')
        dates=request.GET.get('month')
        dates=dates.split("-")
        month=dates[0]
        year=dates[1]
        salesreport=selector.get_sales_call_report_monthly(month,year,repId)
        return JsonResponse({"report":salesreport})
    else:
        return redirect('/login')
#print Sales call Report
def print_sales_call_report(request):
    if 'UserId' in request.session: 
        repId=request.GET.get('SalesRep')
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        salesreport,interested=selector.get_sales_call_report(from_date,to_date,repId)
        if salesreport:
            total_row=salesreport[-1]
            spoken=total_row[1]
            total=total_row[6]
            spokenper=round((spoken/total)*100,2)
        
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
        
def ticket_summary(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        # pending=selector.load_ticket_summary_pending(userid)

        return render(request,'sales/ticketsummary.html')  
    else:
        return redirect('/login')

def ticket_summary_onload(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        pending,resolved,dormant=selector.load_ticket_summary(userid)

        return JsonResponse({"pending":pending,"resolved":resolved,"dormant":dormant})  
    else:
        return redirect('/login')

def complaint_details(request):
    if 'UserId' in request.session:
        complaint_id=request.GET.get('id')
        details=selector.get_complaint_details(complaint_id)
        return JsonResponse({"details":details})
    else:
        return redirect('/login')
def detailed_complaints(request):
    if 'UserId' in request.session:
        
        details=selector. get_all_complaints()
        return render(request,'compliance/details.html',{'complaints':details})
    else:
        return redirect('/login')
def complaint_update(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        complaint_id=request.GET.get('id')
        status=request.GET.get('status')
        desc=request.GET.get('desc')
        message=selector.edit_complaint_details(complaint_id,status,desc,userid)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')
def mailto_complaint_client(request):
    if 'UserId' in request.session:
        message="Please try again"
        complaint_id=request.GET.get('id')
        name=request.GET.get('name')
        client_email=request.GET.get('email')
        description=request.GET.get('description')
        message=emailservice.complaint_client(complaint_id,name,client_email,description)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')
def inactivetickets(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        sourcelist=selector.get_sources()
        salesrep=selector.get_salesrep_permission(userid)
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        inactive=selector.inactive_tickets_default("1900-09-19",date_today,0,"")
        return render(request,'management/inactivetickets.html',{'sources':sourcelist,'salesrep':salesrep,'inactives':inactive})
    else:
        return redirect('/login')
def inactiveticketLoad(request):
    if 'UserId' in request.session:
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        source=request.GET.get('source')
        rep=request.GET.get('repId')
        if rep:
            rep=int(rep)
        else:
            rep=0
        print("Inputs=====",from_date,to_date,rep,source)
        inactive=selector.inactive_tickets_default(from_date,to_date,rep,source)
        return JsonResponse(inactive,safe=False)
    else:
        return redirect('/login')

def livechatreport(request):
    if 'UserId' in request.session:
        reps=selector.get_livechat_reps()
        users=selector.get_livechat_users()
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        print("Form data=======",date_today)
        livechat=selector.get_live_chat_logs("2022-05-03",date_today,0,0)
        print("Live chat=====",livechat)
        return render(request,'management/livechatreport.html',{'reps':reps,'users':users,'chats':livechat})
    else:
        return redirect('/login')
#Live chat report load all
def livechatreport_load_all(request):
    if 'UserId' in request.session:
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        attend=request.GET.get('attend')
        rep=request.GET.get('repId')
        livechat=selector.get_live_chat_logs(from_date,to_date,rep,attend)
        print("Live chat=====",livechat)
        return JsonResponse(livechat,safe=False)
    else:
        return redirect('/login')
#New Account from side bar and New Account Funded Today from dashboard
def new_accounts(request):
    active="Live"
    if 'UserId' in request.session:
        try:
            Cursor=connection.cursor()
            change=request.GET.get('change')
            role=request.session.get("role")
            status=request.GET.get('status')
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                    date_yesterday = datetime.today()-timedelta(3)
            else:
                    date_yesterday = datetime.today()-timedelta(1)
            #date_yesterday = "1900-01-01"
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            accounts_data=selector.get_new_accounts_click("FundedLive",date_yesterday,date_today)#get_new_accounts_filter
            
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"FundedLive"])
            live_funded_today=Cursor.fetchone()
            if live_funded_today:
                live_funded_today=live_funded_today[0]
            
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"NonFundedLive"])
            live_nonfund=Cursor.fetchone()
            if live_nonfund:
                live_nonfund=live_nonfund[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"TempApprovedPending"])
            pending_approved=Cursor.fetchone()
            if pending_approved:
                pending_approved=pending_approved[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday,date_today,"WaitingApprovalPending"])
            pending_waiting=Cursor.fetchone()
            if pending_waiting:
                pending_waiting=pending_waiting[0]
            # if(change=='fundToday'):
            #     funded_count,nonfunded_count,funded_clients,date_today,date_yesterday=selector.funded_today()
            # if(change=='fundWeekly'):
            #     funded_count,nonfunded_count,funded_clients,date_today,date_yesterday=selector.funded_weekly()
            # if(change=='nonfudTotal'):
            #     funded_count,nonfunded_count,funded_clients,date_today,date_yesterday=selector.nonfunded_weekly()
            # else:
            #     funded_count,nonfunded_count,funded_clients,date_today,date_yesterday=selector.funded_today()
                
            
            accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return render(request,'sales/newAccounts.html',{'accounts_data':accounts_data,'from':date_yesterday,'to':date_today,'fundcount':live_funded_today,'nonfundcount':live_nonfund,'accounts_count':accounts_count,"active":json.dumps(active),'role':json.dumps(role)})
        
    else:
        return redirect('/login')

#Existing Accounts
def existing_accounts(request):
    active="Exist"
    if 'UserId' in request.session:
        funded_clients=[]
        date_today=""
        date_yesterday=""
        change=request.GET.get('change')
        role=request.session.get("role")
        print("Existing======================",change)
        if(change=='fundToday'):
            funded_clients,date_today,date_yesterday=selector.existing_funded_today()
        if(change=='fundWeekly'):
            funded_clients,date_today,date_yesterday=selector.existing_funded_week()
        if(change=='nonfundTotal'):
            funded_clients,date_today,date_yesterday=selector.existing_nonfunded_total()
        
            
        print("Exist====",funded_clients)
        accounts_count=selector.get_new_accounts_count(date_yesterday,date_today)
        return render(request,'sales/newAccounts.html',{'accounts_data':funded_clients,'from':date_yesterday,'to':date_today,'accounts_count':accounts_count,"active":json.dumps(active),'role':json.dumps(role)})
        
    else:
        return redirect('/login')
#new accounts funded click
def new_accounts_funded_click(request):
    active="Live"
    if 'UserId' in request.session:
        try:
            Cursor=connection.cursor()
            change=request.GET.get('change')
            status=request.GET.get('status')
            from_date=request.GET.get('from')
            to_date=request.GET.get('to')
            print("HEHEHEHEHE",status,from_date,to_date)
            
            if(status=="Funded" or change=="Live"):
                accounts_data=selector.get_new_accounts_click("FundedLive",from_date,to_date)#get_new_accounts_filter
            
            if(status=="NonFunded"):
                accounts_data=selector.get_new_accounts_click("NonFundedLive",from_date,to_date)#get_new_accounts_filter
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[from_date,to_date,"FundedLive"])
            live_funded_today=Cursor.fetchone()
            if live_funded_today:
                live_funded_today=live_funded_today[0]
            
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[from_date,to_date,"NonFundedLive"])
            live_nonfund=Cursor.fetchone()
            if live_nonfund:
                live_nonfund=live_nonfund[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[from_date,to_date,"TempApprovedPending"])
            pending_approved=Cursor.fetchone()
            if pending_approved:
                pending_approved=pending_approved[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[from_date,to_date,"WaitingApprovalPending"])
            pending_waiting=Cursor.fetchone()
            if pending_waiting:
                pending_waiting=pending_waiting[0]
                
            # if(status=="Funded" or status=="Live"):
            #     funded_count,nonfunded_count,funded_clients,date_today,date_yesterday=selector.funded_by_date(from_date,to_date)

            # else:
            #      funded_count,nonfunded_count,funded_clients,date_today,date_yesterday=selector.nonfunded_by_date(from_date,to_date)
            
            # funded_clients=ClentsSerializer(funded_clients,many=True).data
            # print("Accounts data===",funded_clients,funded_count,nonfunded_count)
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return HttpResponse(json.dumps({"data":accounts_data,'fundcount':live_funded_today,'nonfundcount':live_nonfund,'approved':pending_approved,'waiting':pending_waiting,'to':to_date,'from':from_date},default=str), content_type="application/json")
        
                
    else:
        return redirect('/login')
#new accounts funded click
def ext_accounts_funded_click(request):
    active="Live"
    if 'UserId' in request.session:
        status=request.GET.get('status')
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        print("HEHEHEHEHE",status,from_date,to_date)
       
        funded_clients,date_today,date_yesterday=selector.existing_funded_click(from_date,to_date)

       
        
        funded_clients=ClentsSerializer(funded_clients,many=True).data
        print("Accounts data===",funded_clients)
        return HttpResponse(json.dumps({"data":funded_clients}), content_type="application/json")
        
                
    else:
        return redirect('/login')




def salescampaigns(request):
    if 'UserId' in request.session:
        last_campaign_id=0
        country_id=0
        total_ticket=0
        registerd_live=0
        interested_not=0
        spoken_count=0
        registerd_live=0
        started_training=0
        unattended=0
        campaigns=selector.get_campaigns()
        latestwebinar=selector.get_latest_seminar()
        if campaigns:
            last_campaign=campaigns[-1]
            last_campaign_id=int(last_campaign[0])
        sourcelist=selector.get_sources()    
        country_list=selector.get_all_country()
        report=selector.get_campaigns_report(last_campaign_id,country_id)
        if report:
            for alldata in report:
                if(alldata[0]!="Not Created"):
                    total_ticket=total_ticket+1
                if(alldata[0]=="Not Created"):
                    unattended=unattended+1
                if(alldata[3]!=""):
                    registerd_live=registerd_live+1
                if(alldata[4]!="Not Interested"): 
                    interested_not=interested_not+1
                if(alldata[6]!="No"):
                    spoken_count=spoken_count+1
                if(alldata[8]!="No"):
                    started_training=started_training+1
                
              
        return render(request,'management/salescampaigns.html',{'campaigns':campaigns,'countryList':country_list,'reports':report,'total':total_ticket,'unattended':unattended,'registerlive':registerd_live,'interested':interested_not,'spoken_count':spoken_count,'training':started_training,'latestwebinar':latestwebinar,'sources':sourcelist})
    else:
        return redirect('/login')

def load_sales_campaign(request):
    if 'UserId' in request.session:
        source=request.GET.get("campaign")
        country=request.GET.get("country")
        
        total_ticket=0
        registerd_live=0
        interested_not=0
        spoken_count=0
        registerd_live=0
        started_training=0
        unattended=0
        report=selector.get_campaigns_report(source,country)
        if report:
            for alldata in report:
                
                if(alldata[0]!="Not Created"):
                    total_ticket=total_ticket+1
                if(alldata[0]=="Not Created"):
                    unattended=unattended+1
                if(alldata[3]!=""):
                    registerd_live=registerd_live+1
                if(alldata[4]!="Not Interested"): 
                    interested_not=interested_not+1
                if(alldata[6]!="No"):
                    spoken_count=spoken_count+1
                if(alldata[8]!="No"):
                    started_training=started_training+1
       
        return  HttpResponse(json.dumps({"reports":report,"total":total_ticket,"unattended":unattended,"registerlive":registerd_live,"interested":interested_not,"spoken_count":spoken_count,"training":started_training},default=str),content_type="application/json")
    else:
        return redirect('/login')
    #Funded accounts
def funded_accounts(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        userrole=request.session.get('role')
        ticketlist=[]
        details=""
        funded=list(TblEwalletTransaction.objects.using('svg').filter(trans_status=1,trans_type=1).values_list('accnt_no').distinct())
        
        for data in funded:
            accountno=data[0]
            
            get_tickets=TblClients.objects.filter(login=accountno)
            for tickets in get_tickets.iterator():
                ticket=tickets.ticket
                ticketlist.append(ticket)
            
        
        
        if(userrole=='salesrep'):
            details=list(TblSaleslead.objects.filter(ticket_no__in=ticketlist,salesrepid=userid))
        else:
            details=list(TblSaleslead.objects.filter(ticket_no__in=ticketlist))
            
        
        return render(request,'sales/funded.html',{'details':details})
    
    else:
        return redirect('/login')

#Assign to manager
def assign_to_manager(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        
        managerid=TblUser.objects.filter(username="online").only('userid').first()
        reassignticket=TblSaleslead.objects.get(ticket_no=ticket)
        reassignticket.salesrepid=managerid
        reassignticket.save()
        emailservice.reassign_to_manager(ticket) 
        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')
#Reminder for nonfunded tickets
def remind_rep_nonfunded(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        print("Ticket=======",ticket)
        emailservice.mail_after_one_week(ticket)
        return JsonResponse({"message":"success"})
    else:
        return redirect('/login')
#Compliance manage Acccount
def compliance_manage_accounts(request):
    if 'UserId' in request.session:
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        nationality=selector.load_nationality()
        country=selector.get_all_country()
        leverage=selector.loadLeverage()
        accountType=selector.loadAccountType()
        risk=selector.loadRiskCategory()
        groups=selector.loadgroups(user,server,password)
        print("type of grous===",type(groups))
        return render(request,'compliance/manageaccountnew.html',{"nations":nationality,'country_list':country,'leverage':leverage,'account':accountType,'risks':risk, 'groups':groups})
    else:
        return redirect('/login')
#File CSV upload
def upload_csv_file(request):
    if 'UserId' in request.session:
        message=""
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            message="Please Upload CSV"
        if csv_file.multiple_chunks():
            message="File is too big"
        file_data = csv_file.read().decode("utf-8")		
        lines = file_data.split("\n")
        for line in lines:						
            fields = line.split(",")
            data_dict = {}
            data_dict["name"]=fields[0]
            data_dict["email"]=fields[1]
            data_dict["phone"]=fields[2]
            data_dict["country"]=fields[3]
            data_dict["source"]=fields[4]
            data_dict["status"]=fields[5]
            

        return JsonResponse({"message":message})	
    else:
        return redirect('/login')   























    












   