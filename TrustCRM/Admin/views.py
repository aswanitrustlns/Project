from distutils.log import error
import email
from ipaddress import ip_address
from sqlite3 import Cursor
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from django.contrib.sessions.models import Session
from django.template import Context
import json
import ctypes as ctypes
import instaloader
import os
import subprocess

import socket

insta_username = "Tc_limited"
insta_password = "T@Cmited21!!"
all_data={}

# Load_Insta=instaloader.Instaloader()
Cursor=connection.cursor()

# Create your views here.

def login(request):
    
    # try:
    #     Cursor.execute("SP_GetDesignation")
    #     user_role=Cursor.fetchall()
    # finally:
    #     Cursor.close()
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
        Cursor.execute("set nocount on;exec SP_GetLoginDetails %s",[username])
        UserId=Cursor.fetchone()
        UserId=UserId[0]
        # print("user Id")
        # print(type(UserId))

        request.session['UserId'] = UserId
    except:
        connect=0
        msg="User not Found"
        request.session["message"]=msg
    
 
        # pwd -- Tc2022
    connect=subprocess.call(["C:\\Aswani\\pythonmanager\\manager_python.exe","1",server_name,username,password])
    print(connect)
    if(connect==0):    
            return redirect('dashboard/')
    else:
        request.session["message"]=msg
        return render(request,'admin/login.html',{'login_error':msg})


def dashboard(request):
    print("dashboard-start",datetime.now().time())
    UserId=request.session.get('UserId')
    global all_data
    seminar_weekly_pie=[]
    meeting_daily_pie=[]
    meeting_weekly_pie=[]
    daily_live_bar=[]
    weekly_live_bar=[]
    status_bar=[]
    seminar_daily_pie=[]
    halfyearly_bar=[]
    insta_follwers_list=[]
    count=0
    date_today=datetime.today().date()
    week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
    date_today=date_today.strftime("%Y-%m-%d")
    date_yesterday = datetime.today()-timedelta(1)
    date_yesterday=date_yesterday.strftime("%Y-%m-%d")
    print (date_yesterday)

    try:
        Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[UserId])
        UserName=Cursor.fetchone()
        request.session['UserName']=UserName[0]
        if(week_day==0):
            date_yesterday = datetime.today()-timedelta(3)
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")

        
        Cursor.execute("{call dbo.SP_GetDashboardCount(%s,%s,%s)}", [UserId,date_yesterday,date_today])
             
        result_set = Cursor.fetchall()        
       
        
        Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'w')           
        weekly_live_account = Cursor.fetchall()  
        
        Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'d')           
        livecount_daily = Cursor.fetchall()

        Cursor.execute("set nocount on;exec SP_GetPermissions %s",[UserId])
        permission_check=Cursor.fetchone()
        # manager=permission_check[11]
        manager=permission_check[11]
        salesRep=permission_check[22]
        # salesRep=True
        print("Permision manager",manager)
        print("Permision",salesRep)
        if manager:
            Cursor.execute("set nocount on; exec SP_OwnLeadsCountTotal")
            leads=Cursor.fetchone()
            leads=leads[1]
            
            Cursor.execute("set nocount on; exec SP_LiveAccountsCountByRepTotalD")           
            live_account = Cursor.fetchone()
            live_account=live_account[1]
            
            
            Cursor.execute("set nocount on;exec SP_MeetingsCountByRepTotal")           
            meetingcount = Cursor.fetchone()
            meetingcount=meetingcount[1]
            
            Cursor.execute("set nocount on; exec SP_SpokenCallsTotal")
            spokencall_one=Cursor.fetchone()
            spokencall_one=spokencall_one[1]
            
            
            
            # UserName="Firaz Monzer"
            

            

        if salesRep:

        # Change
            print("Inside salesrep")
            Cursor.execute("set nocount on;exec SP_OwnLeadsCount")
            leads_sales=Cursor.fetchall()
            leads_sales_len=len(leads_sales)
            for i in range(leads_sales_len):                
                all_leads=leads_sales[i]
                users_name=all_leads[0]
                print(users_name)
                print(UserName)
                if users_name.casefold() == UserName.casefold():
                    print("same username-------------------------------------------------------------------------------------")
                    leads=all_leads[1]
                    break


            
            # Cursor.execute("set nocount on;exec exec SP_LiveAccountsCountByRepWeekly %s",['w'])           
            # live_account_test = Cursor.fetchall()
            Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",['w'])           
            live_account_sales = Cursor.fetchall()
            live_account_sales_len=len(live_account_sales)          
            for i in range(live_account_sales_len):
                print(live_account_sales[i])
                all_names=live_account_sales[i]
                users_name=all_names[0]
                if users_name==UserName:
                    live_account=all_names[1]
                    
            
            Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",['w'])           

            meetingcount_sales = Cursor.fetchall()
            meetingcount_sales_len=len(meetingcount_sales)          
            for i in range(meetingcount_sales_len):
                print(meetingcount_sales[i])
                all_names=meetingcount_sales[i]
                users_name=all_names[0]
                if users_name==UserName:
                    meetingcount=all_names[1]



            Cursor.execute("set nocount on;exec SP_SpokenCallsCount")
            spokencall_one_sales=Cursor.fetchall()
            spokencall_one_sales_len=len(spokencall_one_sales)          
            for i in range(spokencall_one_sales_len):
                print(spokencall_one_sales[i])
                all_names=spokencall_one_sales[i]
                users_name=all_names[0]
                if users_name==UserName:
                    spokencall_one=all_names[1]
        # 88888888888888888888888888888888888888888888888888888
        
        Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'d')           
        meetingcount_daily = Cursor.fetchall()
        
        Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'w')           
        meetingcount_weekly = Cursor.fetchall()
        
        Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'D')           
        seminarcount_daily = Cursor.fetchall()
        
        Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'W')           
        seminarcount_weekly = Cursor.fetchall()
        
        
        
        Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[UserId])
        journel=Cursor.fetchall()
        
        Cursor.execute("set nocount on;exec SP_SalesCallsSummary %s",[UserId])
        leads_pie=Cursor.fetchone()
        leads_pie=leads_pie[:-1]
        
        Cursor.execute("exec SP_GetSummaryToday  %s",[UserId])
        # notification1=Cursor.fetchone()
        # notification2=Cursor.nextset()
       
        notification=Cursor.fetchall()
        print("Notification-------------",notification)
        while (Cursor.nextset()):
            notification_count = Cursor.fetchall()
            print("Notification count-------",notification_count)
        
       
        notify_count=notification_count[0]
        # notification_data=notify_count[1]
        print("Notification Count------------",notify_count)
        # print("Notification data-----------",notification_data)
        # notification_count=len(notification)
        # print("notifiaction",notification,notification_count)
        notification_count=notify_count[0]
        print("**************************",notification_count)
        
        request.session['notification'] = notification_count
        # request.session['notification_data'] = notification_data
       
        Cursor.execute("set nocount on;exec SP_SpokenCallsCount")
        spokencall=Cursor.fetchall()
     
        Cursor.execute("set nocount on;exec SP_GetMeetings")
        all_meetings=Cursor.fetchall()
       
        
        Cursor.execute("set nocount on;exec SP_GetMonthlyCount")
        monthly_count=Cursor.fetchall()
       
        
        Cursor.execute("set nocount on;exec SP_GetLeadsStatusGraph")
        status_graph=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_GetActiveUsers")
        active_users=Cursor.fetchall()
       
        
        Cursor.execute("set nocount on;exec SP_GetActiveCampaigns")
        active_campaigns=Cursor.fetchall()
      
        
        active_campaigns_count=len(active_campaigns)
        
        # Cursor.execute("set nocount on;exec SP_TicketsDialedSummary")
        # ticket_dialed=Cursor.fetchall()
        # Cursor.execute("set nocount on;exec SP_TicketsInterestedSummary")
        # ticket_processed=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_GetHalfyearlySummary_PY")
        halfyearly_data=Cursor.fetchall()
        print("procedurecall-end",datetime.now().time())
        
        # Load_Insta.login(insta_username, insta_password)
        # profile = instaloader.Profile.from_username(Load_Insta.context, insta_username)

        # for follower in profile.get_followers():
        #     insta_follwers_list.append(follower.username)    
        #     count = count + 1
       
        if all([x[1]==0 for x in seminarcount_daily]):
            print("No Count")
        else:
             for seminar in seminarcount_daily:            
                seminar_daily_pie.append(
                        {                
                        'name':seminar[0],
                        'value':seminar[1]
                        }
                    
                )
        if all([x[1]==0 for x in seminarcount_weekly]):
            print("No weekly data")
        else:
             for obj in seminarcount_weekly:            
                seminar_weekly_pie.append(
                        {                
                        'name':obj[0],
                        'value':obj[1]
                        }
                    
                )
        
        
        if all([x[1]==0 for x in meetingcount_daily]):
            print("No weekly data")
        else:
             for meeting in meetingcount_daily:
                meeting_daily_pie.append({
                    'name': meeting[0],
                    'value':meeting[1]

                })

        if all([x[1]==0 for x in meetingcount_weekly]):
            print("No weekly data")
        else:
            for meetings in meetingcount_weekly:
                meeting_weekly_pie.append({
                    'name': meetings[0],
                    'value':meetings[1]

                })
        
       
       
       
        
        for report in weekly_live_account:
            weekly_live_bar.append({
                'name': report[0],
                'value':report[1]

            })
        for daily_report in livecount_daily:
            daily_live_bar.append({
                'name': daily_report[0],
                'value':daily_report[1]

            })
        for status in status_graph:
           status_bar.append({
                'name': status[0],
                'src_count':status[1],
                'ticket_count':status[2]


            })
       
        for data in halfyearly_data:
           halfyearly_bar.append({

                'month': data[1],
                'live_account':data[3],
                'pending_account':data[4],
                'funded_account':data[5],
                'tickets':data[6],
                'leads':data[7]


            })
        
        
        
        
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)    
   
    
    # return HttpResponse(result_set,200)
    print("notification")
    
    print("template-render",datetime.now().time())
    all_data={'username':UserName[0],'overview':result_set,'livecount_daily':json.dumps(livecount_daily),'leads':leads,
    'live_account':live_account,'meeting_count':meetingcount,'spoken_call_one':spokencall_one,
    'spoken_call':spokencall,'all_meetings':all_meetings,'meetingcount_daily':meetingcount_daily,
    'seminarcount_daily':seminarcount_daily,'monthly_count':monthly_count,'active_users':active_users,
    'seminarcount_weekly':seminarcount_weekly,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,
    'weekly_live_account':weekly_live_bar,'daily_live_account':daily_live_bar,'leads_status':status_bar,'journels':journel,'active_campaigns':active_campaigns,'active_campaigns_count':active_campaigns_count,
    'leads_pie':json.dumps(leads_pie),'halfyearly_bar':halfyearly_bar,'insta_followers':insta_follwers_list,'insta_count':count,
    'notification':notification,'notification_count':notification_count}
    return render(request,'admin/dashboard.html',all_data)

def lead(request):
    UserId=request.session.get('UserId')
    print(UserId)
    date_today=datetime.today().date()    
    date_today=date_today.strftime("%Y-%m-%d")
    week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
    if(week_day==0):
            date_yesterday = datetime.today()-timedelta(3)
    else:
        date_yesterday = datetime.today()-timedelta(1)
            
    date_yesterday=date_yesterday.strftime("%Y-%m-%d")
    # Cursor.execute("exec SP_GetTotalLeadsCount %s,%s,%s,%s,%s,%s,%s",[date_yesterday,date_today,'','',0,0,1])
    # leads_count_list=Cursor.fetchall()  
    # leads_count=leads_count_list[0] 
    # leads_count=leads_count[0]
    # print(leads_count)
    Cursor.execute("exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",[date_yesterday,date_today,'',0,0,'',0])
    leads_data=Cursor.fetchall()
    # print("Leads data---------------------",leads_data)
    return render(request,'admin/Leads.html',{'leads_data':leads_data})

def lead_registration(request):
    UserId=request.session.get('UserId')
    print(UserId)
    # Cursor.execute(''' SELECT * FROM tbl_Country''')
    # country_code=Cursor.fetchall()
    Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[UserId])
    UserName=Cursor.fetchone()
    print(UserName[0])
    return render(request,'admin/LeadRegistration.html',{"source":UserName[0]})

def lead_registration_check(request):
    
    UserId=request.session.get('UserId') # Read Session data
    
    if request.is_ajax():
        title=request.POST['title']
        name=request.POST.get('name')
        age=request.POST.get('age')
        email_avl=request.POST.getlist('email_agree')
        email1=request.POST.get('email1')
        email2=request.POST.get('email2')
        mobile=request.POST.get('mobile')
        telephone=request.POST.get('telephone')
        profession=request.POST.get('profession')
        subject=request.POST.get('subject')
        
        state=request.POST.get('state')
        address=request.POST.get('address')
        city=request.POST.get('city')
        zip_code=request.POST.get('zipcode')
        if not zip_code:
            zip_code=0
        
        mobile_country_code=request.POST.get('mobile_country')#Get ContryID
        Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[UserId])
        source=Cursor.fetchone()
        source=source[0]
        
        print("Source222",source)
        Cursor.execute("SELECT ID FROM tbl_Country where CCode=%s",[mobile_country_code])
        country1=Cursor.fetchone()
        if country1:
            country1=country1[0]
        telephone_country_code=request.POST.get('tel_country')#Get ContryID
        Cursor.execute("SELECT ID FROM tbl_Country where CCode=%s",[telephone_country_code])
        country2=Cursor.fetchone()
        if country2:
            country2=country2[0]
        
        reg_date=datetime.today().date()
        reg_date=reg_date.strftime("%m-%d-%Y")
        updated_date=datetime.now()
        
        updated_date=updated_date.strftime("%m-%d-%Y %H:%M:%S")
        
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname)
        print("Updated date---------------",updated_date)
        print(country1)
        print(type(country1))
        print(country2)
        print(type(country2))
        print(type(IPAddr))
        print("print------",title,name,email_avl,email1,email2,profession,subject,source,state,address,city,zip_code,mobile,telephone,mobile_country_code,telephone_country_code,country1,country2,IPAddr)

        print("Lead submit ")        
        Cursor.execute("EXEC SP_InsertSalesLeadReg_CRM %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[name,mobile,telephone,email1,email2,address,city,zip_code,source,UserId,updated_date,updated_date,title,profession,"Pending",state,country1,country2,subject,age,IPAddr])
        ticket=Cursor.fetchone() 
           
        ticket=ticket[0]
        hash_check=ticket.find("#")
        ticket=ticket.replace('#','')
        print(hash_check)
        if hash_check>=0:
              
            print("TTTTTTTTTTTTTTTTTicket",ticket)
            print(type(ticket))
            print("email------",email1,type(email1))
            print("email2",email2,type(email2))
            print("mobile----",mobile,type(mobile))
            print("telephone-----",telephone,type(telephone))

            Cursor.execute("set nocount on;exec SP_MergeTicket %s,%s,%s,%s,%s",[ticket,email1,email2,mobile,telephone])
            # merge_ticket=Cursor.fetchone()
            login=0
            Cursor.execute("set nocount on;exec SP_CheckUserPermission_PY %s,%s,%s",[UserId,ticket,login])
            user_permission=Cursor.fetchone() 
            print("User Permissio-------",user_permission)

            user_permission=user_permission[0]
                
                
            
            print("User Permissio-------",user_permission)
            if user_permission:
                print("No permission")
                return JsonResponse({'success':True,'ticket':ticket})
            else:
                return JsonResponse({'success':False,'ticket':ticket})
            
        
        else:
            
             return render(request,'admin/LeadProcessing.html')
            
        # print(merge_ticket)
        
def lead_processing(request):
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
                                                                                                                            
        if email1 or email2 or mobile or phone:
            Cursor.execute("set nocount on;exec SP_SearchPhoneEmail_PY %s,%s,%s,%s,%s",[mobile,phone,email1,email2,UserId]) # To test exec SP_SearchPhone '4588',21
            search_email_phone=Cursor.fetchall() 
            print("--------------------------",search_email_phone,type(search_email_phone))
            while (Cursor.nextset()):
                search_email_phone1 = Cursor.fetchall()
                print("next data set1----------------",search_email_phone1)
            if search_email_phone1:
                search_email_phone=search_email_phone+search_email_phone1
            while (Cursor.nextset()):
                search_email_phone2 = Cursor.fetchall()
                print("next data set2----------------",search_email_phone2)
            if search_email_phone2:
                search_email_phone=search_email_phone+search_email_phone2
            while (Cursor.nextset()):
                search_email_phone3 = Cursor.fetchall()
                print("next data set3----------------",search_email_phone3)
            if search_email_phone3:
                search_email_phone=search_email_phone+search_email_phone3
        if ticket is None:
            ticket=" "
        print("ticket1111111111111111111",ticket)
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)
    return render(request,'admin/LeadProcessing.html',{'ticket':ticket,'email_phone':json.dumps(search_email_phone),'email_phone1':search_email_phone1,'email_phone2':search_email_phone2,'email_phone3':search_email_phone3})
    
   

def logout(request):
    UserId=request.session['UserId']
    del request.session['UserId']
    print("logout")
    print(UserId)
    Cursor.execute("set nocount on;exec SP_SetUserStatus %s",[UserId])
    return redirect('login/')