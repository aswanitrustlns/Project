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
        UserName=selector.get_user_name(UserId)        
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
                if(search_email_phone != None):
                    print("Check it is none")
                    get_ticket=search_email_phone[0]
                    print("Get ticket--------------------",get_ticket)
                    ticket=get_ticket
            
            lead_details,country=selector.get_lead_details(ticket,UserId)
            activity_log=selector.get_activity_log(ticket)
            ticket_summary=selector.get_ticket_summary(ticket)
            lead_score=selector.get_lead_score(ticket)
            meeting_score=selector.get_meeting_score(ticket)
            last_comment=selector.get_last_comment(ticket,UserId)
            sticky_text=selector.get_sticky_text(ticket)
            print("Last comment--------",last_comment)
            
            print("Sticky text============================",sticky_text)
            print("Lead details-------------")
            if(meetingscore !=None):
                print("Meeting if")
                meetingscore=sum(meetingscore)
                meetingscore=(meetingscore/320)*100
                
            print("Meeting score-----------------------",meeting_score)
            page_data={'ticket':ticket,'country':country,'email_phone':json.dumps(search_email_phone),'lead_details':lead_details,'ticket_summary':ticket_summary,'activity_log':activity_log,'leadscore':lead_score,'meetingscore':meeting_score,'lastcomment':last_comment,'stickytext':sticky_text}
            
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)
    
        return render(request,'sales/LeadProcessing.html',{'ticket':ticket,'country':country,'email_phone':json.dumps(search_email_phone),'lead_details':lead_details,'ticket_summary':ticket_summary,'activity_log':activity_log,'leadscore':lead_score,'meetingscore':meeting_score,'lastcomment':last_comment,'stickytext':sticky_text})
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
        print("User idddddddddddddd",UserId)
        pending_tickets=selector.get_tickets(UserId,"pending")
        
        return render(request,'sales/pendingtickets.html',{'pending_tickets':pending_tickets})
    else:
         return redirect('/login') 

def pending_tckts_load_all(request):
    if 'UserId' in request.session:
        UserId=request.session.get('UserId')   
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        print("From date-----------------",from_date)
        print("To date------------------",to_date)
        
        pending_tickets=selector.get_all_tickets(UserId,"pending",from_date,to_date)
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
        salesrepId=56
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

    if 'UserId' in request.session:
        change=request.GET.get("change")
        from_date=request.GET.get("from")
        to_date=request.GET.get("to")
        status=request.GET.get("status")
        print("From date====",from_date)
        print("To_date====",to_date)
        
        print("Status----------------------",status)
        if(change):
            accounts_data=selector.get_new_accounts(change,status,from_date,to_date)
            print("change is---------------",change)
            return JsonResponse(list(accounts_data), safe=False)
        else:
            
            accounts_data=selector.get_new_accounts("Live","",from_date,to_date)
            accounts_count=selector.get_new_accounts_count()
            print("Accounts count-----------",accounts_count)
            # terminated_data=selector.get_new_accounts("Terminated")
            return render(request,'admin/newAccounts.html',{'accounts_data':accounts_data,'accounts_count':accounts_count})
                
    else:
        return redirect('/login')

def sendRemiderMail(request):
    if 'UserId' in request.session:        
        ticket=request.GET.get('ticket')
        subject="Trust Capital - Meeting Reminder"
        bcc=""
        cc=""
        selector.mailSend(ticket,subject,bcc,cc)
        
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

    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        ticket=ticket.strip()
        print("Ticket--------------------------",ticket)
       
        all_meetings=selector.get_all_meeting(ticket)
        print("All meeting----------------",len(all_meetings))
        return render(request,'sales/meeting.html',{'meetings':all_meetings})
    else:
        return redirect('/login')

def send_meeting_request(request):

    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        flag=int(request.GET.get('flag'))
        message=service.send_meeting_request(request)
        message=message[0]   
        print("Flag--------------------",type(flag))     
        if(flag == 0 or flag == 1):
            subject="TC Limited – Meeting Confirmation"
        if(flag == 2):
            print("Meeting cancelled")
            subject = "TC Limited – Meeting Cancelled"
        print("Subject--------------------------------------",subject)
        if(message == 'PROCEED'):
            print("Proceed---")          
            # bcc="crm@trusttc.com"
            bcc="aswani.trustlns@gmail.com"
            cc=" "
            selector.mailSend(ticket,subject,bcc,cc)
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



def saveMeeting(request):
    if 'UserId' in request.session:
        score=service.save_meeting_score(request)
        return JsonResponse({"score":score})
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
        print("Count================================",count)
        print("Endd===================================",count_end)
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
        message_data,subject,sender,count=selector.read_mail_inbox(message)
        return render(request,'sales/inboxread.html',{'message':message_data,'subject':subject,'sender':sender,'count':count})
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
        ticket=request.GET.get('ticket')
        ticket=ticket.strip()
        UserId=request.session.get('UserId')
        activity_log=selector.get_activities_log(ticket)
        lead_details,country=selector.get_lead_details(ticket,UserId)
        leadscore=selector.get_lead_score(ticket)
        last_comment=selector.get_last_comment(ticket,UserId)
        
        ticket_summary=selector.get_ticket_summary(ticket)
        sticky_text=selector.get_sticky_text(ticket)
        print("Last comment--------",last_comment)
        meetingscore=selector.get_meeting_score(ticket)
        print("Meetin score=============================",meetingscore)
        if(meetingscore != None):
            meetingscore=sum(meetingscore)
            meetingscore=(meetingscore/320)*100
            
        print("Meeting score----",meetingscore)
        print("Sticky text========",sticky_text)
        print("End---------------------")
        return JsonResponse({'leads':lead_details,'country':country,'activities':activity_log,'ticket_summary':ticket_summary,'leadscore':leadscore,'meetingscore':meetingscore,'lastcomment':last_comment,'stickytext':sticky_text})
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
        accountNo=request.GET.get('account')
        selector.account_status_check_update(accountNo)
    else:
        return redirect('/login')

#Ticket status update
def ticket_status(request):
    if 'UserId' in request.session:
        ticket=request.POST.get('ticket')
        print("Ticket-------",ticket)
        experience=request.POST.get('experience')
        hear=request.POST.get('hearfrom')
        print("Request===============================================",experience,hear)
        selector.ticket_validity_check_update(ticket,request)
        return JsonResponse({"success"})
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
        return JsonResponse({"Success"})
    else:
        return redirect('/login')

#Manage ticket Email send

def email_send(request):
    if 'UserId' in request.session:   
        fromaddr=request.POST.get('from')
        to=request.POST.get('to')
        name=request.POST.get('name')
        title=request.POST.get('tit')
        sub=request.POST.get('subject')
        emailbody=request.POST.get('body')
        selector.email_compose(fromaddr,to,sub,emailbody)
        return JsonResponse({"success":True})
    else:
        return redirect('/login')

def save_reminder_details(request):
    if 'UserId' in request.session:
        print("Save reminder view=========")
        userid=request.session.get('UserId')
        date=request.POST.get('date')
        time=request.POST.get('time')
        ticket=request.POST.get('ticket')
        subject=request.POST.get('subject')
        if(subject==None):
            subject=" "
        badge=request.POST.get('badge')
        print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",userid,ticket,subject,date,time,badge)
        selector.save_reminder(userid,ticket,subject,date,time,badge)
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
        ticket=request.GET.get('note')
        msg=selector.resolve_ticket(ticket,userid)
        print("Message=========================",msg)
        return JsonResponse({"message":msg})
    else:
        return redirect('/login')
    

    












   