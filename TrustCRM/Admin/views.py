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
import json
import instaloader

import socket

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
# Create your views here.

def login(request):    
    
    msg=" "
    return render(request,'admin/login.html',{'login_error':msg})

def login_check(request):
    print("login-start",datetime.now().time())
    msg="Username and Password do not match"
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        server_name=request.POST['server']
    try:  
           
        UserId=selector.get_loged_user_info(username)   
        request.session['UserId'] = UserId
        connect=selector.exe_connection(username,server_name,password)
        
    except Exception as e:
        print("Exception------------",e.__class__)
        connect=1
        msg="User not Found"
        request.session["message"]=msg        
   
    print(connect)
    if(connect==0):    
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
        UserId=56
        permission_check=selector.user_role_selection(UserId)          
        manager=permission_check[11]
        salesRep=permission_check[22]
        dashbord_data={}
        UserName=selector.get_user_name(UserId)
        notification_count,notification=selector.get_notification_data(UserId)
        request.session['UserName']=UserName
        request.session['notification'] = notification_count
        request.session['notification_data']=notification
     
        if manager:
             dashbord_data=sales_dash.admin_dashboard(UserId)  
             print("dashboard procedure ",datetime.now().time()) 
             return render(request,'admin/dashboard.html',dashbord_data)
        if salesRep:
             dashbord_data=sales_dash.sales_dashboard(UserId)     
             print("sales dashboard procedure end",datetime.now().time()) 
             return render(request,'sales/dashboard.html',dashbord_data)
    else:
         return redirect('/login') 


    # print("dashboard-start",datetime.now().time())
    # if 'UserId' in request.session:
    #     UserId=request.session.get('UserId')
    #     global all_data
    #     seminar_weekly_pie=[]
    #     meeting_daily_pie=[]
    #     meeting_weekly_pie=[]
    #     daily_live_bar=[]
    #     weekly_live_bar=[]
    #     status_bar=[]
    #     seminar_daily_pie=[]
    #     halfyearly_bar=[]
    #     insta_follwers_list=[]
    #     count=0
    #     date_today=datetime.today().date()
    #     week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
    #     date_today=date_today.strftime("%Y-%m-%d")
    #     date_yesterday = datetime.today()-timedelta(1)
    #     date_yesterday=date_yesterday.strftime("%Y-%m-%d")
    #     print (date_yesterday)

    #     try:
    #         Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[UserId])
    #         UserName=Cursor.fetchone()
    #         request.session['UserName']=UserName[0]
    #         if(week_day==0):
    #             date_yesterday = datetime.today()-timedelta(3)
    #             date_yesterday=date_yesterday.strftime("%Y-%m-%d")

    #         print (date_yesterday)
    #         Cursor.execute("{call dbo.SP_GetDashboardCount(%s,%s,%s)}", [UserId,date_yesterday,date_today])
                
    #         result_set = Cursor.fetchall()        
        
            
    #         Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'w')           
    #         weekly_live_account = Cursor.fetchall()  
            
    #         Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'d')           
    #         livecount_daily = Cursor.fetchall()

    #         permission_check=selector.user_role_selection(UserId)
            
    #         manager=permission_check[11]
    #         salesRep=permission_check[22]
    #         # salesRep=True
    #         print("Permision manager",manager)
    #         print("Permision",salesRep)
    #         if manager:
    #             Cursor.execute("set nocount on; exec SP_OwnLeadsCountTotal")
    #             leads=Cursor.fetchone()
    #             leads=leads[1]
                
    #             Cursor.execute("set nocount on; exec SP_LiveAccountsCountByRepTotalD")           
    #             live_account = Cursor.fetchone()
    #             live_account=live_account[1]
                
                
    #             Cursor.execute("set nocount on;exec SP_MeetingsCountByRepTotal")           
    #             meetingcount = Cursor.fetchone()
    #             meetingcount=meetingcount[1]
                
    #             Cursor.execute("set nocount on; exec SP_SpokenCallsTotal")
    #             spokencall_one=Cursor.fetchone()
    #             spokencall_one=spokencall_one[1]
                
                
                
    #             # UserName="Firaz Monzer"
                

                

    #         if salesRep:

    #         # Change
    #             print("Inside salesrep")
    #             Cursor.execute("set nocount on;exec SP_OwnLeadsCount")
    #             leads_sales=Cursor.fetchall()
    #             leads_sales_len=len(leads_sales)
    #             for i in range(leads_sales_len):                
    #                 all_leads=leads_sales[i]
    #                 users_name=all_leads[0]
    #                 print(users_name)
    #                 print(UserName)
    #                 if users_name.casefold() == UserName.casefold():
    #                     print("same username-------------------------------------------------------------------------------------")
    #                     leads=all_leads[1]
    #                     break


                
    #             # Cursor.execute("set nocount on;exec exec SP_LiveAccountsCountByRepWeekly %s",['w'])           
    #             # live_account_test = Cursor.fetchall()
    #             Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",['w'])           
    #             live_account_sales = Cursor.fetchall()
    #             live_account_sales_len=len(live_account_sales)          
    #             for i in range(live_account_sales_len):
    #                 print(live_account_sales[i])
    #                 all_names=live_account_sales[i]
    #                 users_name=all_names[0]
    #                 if users_name==UserName:
    #                     live_account=all_names[1]
                        
                
    #             Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",['w'])           

    #             meetingcount_sales = Cursor.fetchall()
    #             meetingcount_sales_len=len(meetingcount_sales)          
    #             for i in range(meetingcount_sales_len):
    #                 print(meetingcount_sales[i])
    #                 all_names=meetingcount_sales[i]
    #                 users_name=all_names[0]
    #                 if users_name==UserName:
    #                     meetingcount=all_names[1]



    #             Cursor.execute("set nocount on;exec SP_SpokenCallsCount")
    #             spokencall_one_sales=Cursor.fetchall()
    #             spokencall_one_sales_len=len(spokencall_one_sales)          
    #             for i in range(spokencall_one_sales_len):
    #                 print(spokencall_one_sales[i])
    #                 all_names=spokencall_one_sales[i]
    #                 users_name=all_names[0]
    #                 if users_name==UserName:
    #                     spokencall_one=all_names[1]
    #         # 88888888888888888888888888888888888888888888888888888
            
    #         Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'d')           
    #         meetingcount_daily = Cursor.fetchall()
            
    #         Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'w')           
    #         meetingcount_weekly = Cursor.fetchall()
            
    #         Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'D')           
    #         seminarcount_daily = Cursor.fetchall()
            
    #         Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'W')           
    #         seminarcount_weekly = Cursor.fetchall()
            
            
            
    #         Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[UserId])
    #         journel=Cursor.fetchall()
            
    #         Cursor.execute("set nocount on;exec SP_SalesCallsSummary %s",[UserId])
    #         leads_pie=Cursor.fetchone()
    #         leads_pie=leads_pie[:-1]
            
    #         Cursor.execute("exec SP_GetSummaryToday  %s",[UserId])
    #         # notification1=Cursor.fetchone()
    #         # notification2=Cursor.nextset()
        
    #         notification=Cursor.fetchall()
    #         print("Notification-------------",notification)
    #         while (Cursor.nextset()):
    #             notification_count = Cursor.fetchall()
    #             print("Notification count-------",notification_count)
            
        
    #         notify_count=notification_count[0]
    #         # notification_data=notify_count[1]
    #         print("Notification Count------------",notify_count)
          
    #         notification_count=notify_count[0]
    #         print("**************************",notification_count)
            
    #         request.session['notification'] = notification_count
    #         # request.session['notification_data'] = notification_data
        
    #         Cursor.execute("set nocount on;exec SP_SpokenCallsCount")
    #         spokencall=Cursor.fetchall()
        
    #         Cursor.execute("set nocount on;exec SP_GetMeetings")
    #         all_meetings=Cursor.fetchall()
        
            
    #         Cursor.execute("set nocount on;exec SP_GetMonthlyCount")
    #         monthly_count=Cursor.fetchall()
        
            
    #         Cursor.execute("set nocount on;exec SP_GetLeadsStatusGraph")
    #         status_graph=Cursor.fetchall()
    #         Cursor.execute("set nocount on;exec SP_GetActiveUsers")
    #         active_users=Cursor.fetchall()
        
            
    #         Cursor.execute("set nocount on;exec SP_GetActiveCampaigns")
    #         active_campaigns=Cursor.fetchall()
        
            
    #         active_campaigns_count=len(active_campaigns)
            
         
    #         Cursor.execute("set nocount on;exec SP_GetHalfyearlySummary_PY")
    #         halfyearly_data=Cursor.fetchall()
    #         print("procedurecall-end",datetime.now().time())
            
    #         # Load_Insta.login(insta_username, insta_password)
    #         # profile = instaloader.Profile.from_username(Load_Insta.context, insta_username)

    #         # for follower in profile.get_followers():
    #         #     insta_follwers_list.append(follower.username)    
    #         #     count = count + 1
        
    #         if all([x[1]==0 for x in seminarcount_daily]):
    #             print("No Count")
    #         else:
    #             for seminar in seminarcount_daily:            
    #                 seminar_daily_pie.append(
    #                         {                
    #                         'name':seminar[0],
    #                         'value':seminar[1]
    #                         }
                        
    #                 )
    #         if all([x[1]==0 for x in seminarcount_weekly]):
    #             print("No weekly data")
    #         else:
    #             for obj in seminarcount_weekly:            
    #                 seminar_weekly_pie.append(
    #                         {                
    #                         'name':obj[0],
    #                         'value':obj[1]
    #                         }
                        
    #                 )
            
            
    #         if all([x[1]==0 for x in meetingcount_daily]):
    #             print("No weekly data")
    #         else:
    #             for meeting in meetingcount_daily:
    #                 meeting_daily_pie.append({
    #                     'name': meeting[0],
    #                     'value':meeting[1]

    #                 })

    #         if all([x[1]==0 for x in meetingcount_weekly]):
    #             print("No weekly data")
    #         else:
    #             for meetings in meetingcount_weekly:
    #                 meeting_weekly_pie.append({
    #                     'name': meetings[0],
    #                     'value':meetings[1]

    #                 })
            
        
        
        
            
    #         for report in weekly_live_account:
    #             weekly_live_bar.append({
    #                 'name': report[0],
    #                 'value':report[1]

    #             })
    #         for daily_report in livecount_daily:
    #             daily_live_bar.append({
    #                 'name': daily_report[0],
    #                 'value':daily_report[1]

    #             })
    #         for status in status_graph:
    #             status_bar.append({
    #                     'name': status[0],
    #                     'src_count':status[1],
    #                     'ticket_count':status[2]


    #                 })
            
    #         for data in halfyearly_data:
    #             halfyearly_bar.append({

    #                     'month': data[1],
    #                     'live_account':data[3],
    #                     'pending_account':data[4],
    #                     'funded_account':data[5],
    #                     'tickets':data[6],
    #                     'leads':data[7]


    #                 })  
    #         all_data={'username':UserName[0],'overview':result_set,'livecount_daily':json.dumps(livecount_daily),'leads':leads,
    #                     'live_account':live_account,'meeting_count':meetingcount,'spoken_call_one':spokencall_one,
    #                     'spoken_call':spokencall,'all_meetings':all_meetings,'meetingcount_daily':meetingcount_daily,
    #                     'seminarcount_daily':seminarcount_daily,'monthly_count':monthly_count,'active_users':active_users,
    #                     'seminarcount_weekly':seminarcount_weekly,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,
    #                     'weekly_live_account':weekly_live_bar,'daily_live_account':daily_live_bar,'leads_status':status_bar,'journels':journel,'active_campaigns':active_campaigns,'active_campaigns_count':active_campaigns_count,
    #                     'leads_pie':json.dumps(leads_pie),'halfyearly_bar':halfyearly_bar,'insta_followers':insta_follwers_list,'insta_count':count,
    #                     'notification':notification,'notification_count':notification_count}         
            
            
            
    #     except Exception as e:
    #         print("!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)    
    
        
       
    #     print("template-render",datetime.now().time())
        
    #     return render(request,'admin/dashboard.html',all_data)
    # else:
    #      return redirect('/login') 

def lead(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        print(UserId)
             
        lead="lead"
        leads_data=selector.get_leads(lead)
        # print("Leads data---------------------",leads_data)
        return render(request,'admin/Leads.html',{'leads_data':leads_data})
    else:
         return redirect('/login') 

def lead_load_all(request): 
    
    lead="all"
    load_data=selector.get_leads(lead)   
    # paginator = Paginator(load_data, 10)
    print("load data-------------------------",len(load_data))
    return JsonResponse(load_data, safe=False)

def new_accounts(request):
    if 'UserId' in request.session:
        new_accounts_data=selector.get_new_accounts()
        print("New Accounts page data")
        # return render(request,'admin/newaccounts.html',{'page_data':new_accounts_data})
    else:
         return redirect('/login')

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
        UserName=selector.get_user_name(UserId)        
        return render(request,'admin/LeadRegistration.html',{"source":UserName})
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
        ticket=" "
        try:
            ticket=request.GET.get('ticket')
            email1=request.GET.get('email1')
            email2=request.GET.get('email2')
            mobile=request.GET.get('mobile')
            phone=request.GET.get('telephone')
            
            print("email1",email1,"email2",email2,"mobile",mobile,"phone",phone)
            if ticket is None:
                ticket=" "                                                                                                                    
            if email1 or email2 or mobile or phone:
                Cursor.execute("set nocount on;exec SP_SearchPhoneEmail_PY %s,%s,%s,%s,%s",[mobile,phone,email1,email2,UserId]) # To test exec SP_SearchPhone '4588',21
                search_email_phone=Cursor.fetchone() 
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
                get_ticket=search_email_phone[0]
                print("Get ticket--------------------",get_ticket)
                ticket=get_ticket

            print("ticket1111111111111111111",ticket)
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)
    
        return render(request,'admin/LeadProcessing.html',{'ticket':ticket,'email_phone':json.dumps(search_email_phone)})
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
        
        pending_tickets=selector.get_tickets(UserId,"pending","load")
        
        return render(request,'admin/pendingtickets.html',{'pending_tickets':pending_tickets})
    else:
         return redirect('/login') 

def pending_tckts_load_all(request):
    UserId=request.session.get('UserId')   
    
    pending_tickets=selector.get_tickets(UserId,"pending","all")
    # paginator = Paginator(load_data, 10)
    print("load data-------------------------",len(pending_tickets))
    return JsonResponse(list(pending_tickets), safe=False)
    

def resolved_tickets(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')
        print(UserId)
        
        resolved_tickets=selector.get_tickets(UserId,"resolved","load")
        
        return render(request,'admin/resolvedtickets.html',{'resolved_tickets':resolved_tickets})
    else:
         return redirect('/login') 


def resolved_tckts_load_all(request):
    UserId=request.session.get('UserId')
    
    resolved_tickets=selector.get_tickets(UserId,"resolved","load")
    # paginator = Paginator(load_data, 10)
    print("load data-------------------------",len(resolved_tickets))
    return JsonResponse(list(resolved_tickets), safe=False)

def new_accounts(request):

    if 'UserId' in request.session:
        change=request.GET.get("change")
        if(change):
            accounts_data=selector.get_new_accounts(change)
            print("change is---------------",change)
            return JsonResponse(list(accounts_data), safe=False)
        else:
            
            accounts_data=selector.get_new_accounts("Live")
            return render(request,'admin/newAccounts.html',{'accounts_data':accounts_data})
                
    else:
        return redirect('/login')

def sendRemiderMail(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        selector.mailSend(ticket)
        return JsonResponse({'success':True})
    else:
        return redirect('/login')
   