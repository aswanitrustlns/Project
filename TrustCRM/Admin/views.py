from ipaddress import ip_address
from sqlite3 import Cursor
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from django.contrib.sessions.models import Session
import json
import ctypes as ctypes
import instaloader
import os
import subprocess

import socket

insta_username = "Tc_limited"
insta_password = "T@Cmited21!!"

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
        
       
        notify_count=notification_count[0]
        # notification_count=len(notification)
        # print("notifiaction",notification,notification_count)
        notification_count=notify_count[0]
        print("notification counrttttt",notification_count[0])
        Cursor.execute("set nocount on;exec SP_SpokenCallsCount")
        spokencall=Cursor.fetchall()
        print("procedurecall-start",datetime.now().time())
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
        Cursor.execute("set nocount on;exec SP_TicketsDialedSummary")
        ticket_dialed=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_TicketsInterestedSummary")
        ticket_processed=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_GetHalfyearlySummary")
        halfyearly_data=Cursor.fetchall()
        print("procedurecall-end",datetime.now().time())
        
        # Load_Insta.login(insta_username, insta_password)
        # profile = instaloader.Profile.from_username(Load_Insta.context, insta_username)

        # for follower in profile.get_followers():
        #     insta_follwers_list.append(follower.username)    
        #     count = count + 1
       
        
        for obj in seminarcount_weekly:            
            seminar_weekly_pie.append(
                    {                
                    'name':obj[0],
                    'value':obj[1]
                    }
                
            )
        for seminar in seminarcount_daily:            
            seminar_daily_pie.append(
                    {                
                    'name':seminar[0],
                    'value':seminar[1]
                    }
                
            )
        for meeting in meetingcount_daily:
            meeting_daily_pie.append({
                'name': meeting[0],
                'value':meeting[1]

            })
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
                'funded_account':data[5]


            })
        
        
        
        
    except:
        print("Exception")    
   
    
    # return HttpResponse(result_set,200)
    print("notification")
  
    print("template-render",datetime.now().time())
    return render(request,'admin/dashboard.html',{'username':UserName[0],'overview':result_set,'livecount_daily':json.dumps(livecount_daily),'leads':leads,
    'live_account':live_account,'meeting_count':meetingcount,'spoken_call_one':spokencall_one,
    'spoken_call':spokencall,'all_meetings':all_meetings,'meetingcount_daily':meetingcount_daily,
    'seminarcount_daily':seminarcount_daily,'monthly_count':monthly_count,'status_graph':status_graph,'active_users':active_users,
    'seminarcount_weekly':seminarcount_weekly,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,
    'weekly_live_account':weekly_live_bar,'daily_live_account':daily_live_bar,'leads_status':status_bar,'journels':journel,'active_campaigns':active_campaigns,
    'leads_pie':json.dumps(leads_pie),'ticket_dialed':ticket_dialed,'ticket_processed':ticket_processed,'halfyearly_bar':halfyearly_bar,'insta_followers':insta_follwers_list,'insta_count':count,
    'notification':notification,'notification_count':notification_count})

def lead(request):
    UserId=request.session.get('UserId')
    print(UserId)
    Cursor.execute("exec SP_GetSummaryListToday  %s",[UserId])
    notification=Cursor.fetchall()   
    print(notification[0])  
    notification=json.dumps(notification) 
    print(notification) 
    print(notification[0])
    
    return render(request,'admin/Leads.html')

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
    UserId=request.session.get('UserId')
    if request.method == 'POST':
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
        updated_date=datetime.today().date()
        updated_date=updated_date.strftime("%m-%d-%Y")
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname)
        print(type(IPAddr))
        print("print------",title,name,email_avl,email1,email2,profession,subject,source,state,address,city,zip_code,mobile,telephone,mobile_country_code,telephone_country_code,country1,country2,IPAddr)
     
        print("Lead submit ")        
        Cursor.execute("EXEC SP_InsertSalesLeadReg_CRM %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[name,mobile,telephone,email1,email2,address,city,zip_code,source,UserId,reg_date,updated_date,title,profession,"Pending",state,country1,country2,subject,age,IPAddr])
        
        ticket=Cursor.fetchone()
        print(ticket)
        print("done")
    return render(request,'admin/Leads.html')
   

def logout(request):
    UserId=request.session['UserId']
    del request.session['UserId']
    print("logout")
    print(UserId)
    Cursor.execute("set nocount on;exec SP_SetUserStatus %s",[UserId])
    return redirect('login/')