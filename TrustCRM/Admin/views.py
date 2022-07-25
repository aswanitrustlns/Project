from sqlite3 import Cursor
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import json
import ctypes as ctypes
import instaloader
import os
import subprocess

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
    return render(request,'admin/login.html')

def login_check(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
    Cursor.execute("set nocount on;exec SP_GetLoginDetails %s",[username])
    UserId=Cursor.fetchone()
    request.session['UserId'] = UserId[0] 
    
        # pwd -- Tc2022
    connect=subprocess.call(["C:\\Aswani\\pythonmanager\\manager_python.exe","1","50.57.14.224:443",'601',password])
    print(connect)
    if(connect==0):    
            return redirect('dashboard/')
    else:
        return redirect('login/')


def dashboard(request):
    UserId=request.session.get('UserId')
    print("USer Iddd")
    print(UserId)
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
    try:
        Cursor.execute("{call dbo.SP_GetDashboardCount(%s,%s,%s)}", [UserId,'2022-07-01','2022-07-19'])
             
        result_set = Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_OwnLeadsCount_PY %s",[UserId])
        leads=Cursor.fetchone()
        Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly_PY %s,%s",['w',UserId])           
        live_account = Cursor.fetchone()      
        Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'w')           
        weekly_live_account = Cursor.fetchall()  
        Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'d')           
        livecount_daily = Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly_PY %s,%s",['w',UserId])           
        meetingcount = Cursor.fetchone()
        Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'d')           
        meetingcount_daily = Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'w')           
        meetingcount_weekly = Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'D')           
        seminarcount_daily = Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'W')           
        seminarcount_weekly = Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_SpokenCallsCount_PY %s",[UserId])
        spokencall_one=Cursor.fetchone()
        Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[UserId])
        journel=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_SalesCallsSummary %s",[UserId])
        leads_pie=Cursor.fetchone()
        leads_pie=leads_pie[:-1]
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
        Cursor.execute("set nocount on;exec SP_TicketsDialedSummary")
        ticket_dialed=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_TicketsInterestedSummary")
        ticket_processed=Cursor.fetchall()
        Cursor.execute("set nocount on;exec SP_GetHalfyearlySummary")
        halfyearly_data=Cursor.fetchall()
        
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
    return render(request,'admin/dashboard.html',{'overview':result_set,'livecount_daily':json.dumps(livecount_daily),'leads':leads[2],
    'live_account':live_account[2],'meeting_count':meetingcount[2],'spoken_call_one':spokencall_one[2],
    'spoken_call':spokencall,'all_meetings':all_meetings,'meetingcount_daily':meetingcount_daily,
    'seminarcount_daily':seminarcount_daily,'monthly_count':monthly_count,'status_graph':status_graph,'active_users':active_users,
    'seminarcount_weekly':seminarcount_weekly,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,
    'weekly_live_account':weekly_live_bar,'daily_live_account':daily_live_bar,'leads_status':status_bar,'journels':journel,'active_campaigns':active_campaigns,
    'leads_pie':json.dumps(leads_pie),'ticket_dialed':ticket_dialed,'ticket_processed':ticket_processed,'halfyearly_bar':halfyearly_bar,'insta_followers':insta_follwers_list,'insta_count':count})

def lead(request):
    
    
    return render(request,'admin/Leads.html')

def lead_registration(request):
    UserId=request.session.get('UserId')
    print(UserId)
    Cursor.execute(''' SELECT * FROM tbl_Country''')
    country_code=Cursor.fetchall()
    Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[UserId])
    UserName=Cursor.fetchone()
    print(UserName[0])
    return render(request,'admin/LeadRegistration.html',{"source":UserName[0]})

def logout(request):
    UserId=request.session['UserId']
    print("logout")
    print(UserId)
    Cursor.execute("set nocount on;exec SP_SetUserStatus %s",[UserId])
    return redirect('login/')