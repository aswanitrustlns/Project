from django.db import connection
from datetime import datetime, timedelta
from .models import TblActionreasons,TblClients,TblEwalletTransaction
from django.db.models import OuterRef, Subquery,Max
from django.db.models import Count
from django.db.models import Q,F
import calendar
import json


class DashboardSelector:

    #----------------------------------------- Sales Dashboard ------------------------------------------------------------------
    
    def sales_dashboard(self,userId):
        # userId=30
        sales_data={}
        weekly_summary_bar=[]
        journel_data=[]
        weekly_lead_bar=[]
        try:
            print("procedure-start1",datetime.now().time())
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetWeeklySummary_PY  %s",[userId])
            weekly_summary=Cursor.fetchall()
            print("--------------------------------------------------------------------------------")
            print("procedure-start2",datetime.now().time())
            Cursor.execute("set nocount on;exec SP_SalesTicketCountByRepWeekly %s,%s",['D',userId])
            ticket_count_daily=Cursor.fetchone()
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday = datetime.today()-timedelta(week_day)
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            print("Yesterday and today======",date_yesterday,date_today)    
            currentMonth = datetime.now().month
            currentYear = datetime.now().year
            start_date=calendar.monthrange(currentYear,currentMonth)
            lastdate=calendar.monthrange(currentYear,currentMonth)[1]
            print("Start date=====",lastdate)
            month_start_date=str(currentYear)+"-"+str(currentMonth)+"-01"
            month_last_date=str(currentYear)+"-"+str(currentMonth)+"-"+str(lastdate)
            print("Month last date===="+month_last_date+"=====first"+month_start_date)
            due_week=TblActionreasons.objects.filter(duedate__date__range=(datetime.strptime(date_yesterday,'%Y-%m-%d'),datetime.strptime(date_today,'%Y-%m-%d')),userid=userId).count()
            due_month=TblActionreasons.objects.filter(duedate__date__gt=datetime.strptime(month_start_date,'%Y-%m-%d'),duedate__date__lt=datetime.strptime(month_last_date,'%Y-%m-%d'),userid=userId).count()
            print("Due week count=====",due_week,due_month)
            # if all([(x[1]==0 and x[2]==0 and x[3]==0)for x in ticket_count_daily]):
            #     ticket_count_daily=[]
            print("procedure-start3",datetime.now().time())
            Cursor.execute("set nocount on;exec SP_SalesTicketCountByRepWeekly %s,%s",['W',userId])
            ticket_count_weekly=Cursor.fetchone()
           
            print("procedure-start4",datetime.now().time()) 
            Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[userId])
            journels=Cursor.fetchall()
            print("procedure-start5",datetime.now().time())                        
            Cursor.execute("set nocount on;exec SP_GetWeeklyLeads_PY")
            leads_converted=Cursor.fetchall()  
            #Meetingsss
            print("procedure-start6",datetime.now().time())
            Cursor.execute("set nocount on;exec SP_GetMeetings %s",[userId])
            meeting_today=Cursor.fetchall() 
            print("Meeting Today=======",meeting_today)
            meeting_count=len(meeting_today)
            if(meeting_count < 9):
                meeting_count=str(meeting_count).zfill(2)
              
            #Reminders....
            print("procedure-start7",datetime.now().time())
            Cursor.execute("exec SP_GetSummaryToday %s",[userId])
            reminders=Cursor.fetchall()

            print("Reminders---------------------------------",reminders)
            while (Cursor.nextset()):
                reminder_count = Cursor.fetchall()
                print("Reminder count-------",reminder_count)
                reminder_count=reminder_count[0]
                reminder_count=reminder_count[0]
            print("Reminder count-------",type(reminder_count))
            reminder_count=int(reminder_count)
            if(reminder_count == 0):
                 reminder_count_show="00"
                 print("reminder count is zero")
            else:
                if(reminder_count < 9 ):
                    reminder_count_show=str(reminder_count)
                    reminder_count_show=reminder_count_show.zfill(2)
                else:
                    reminder_count_show=str(reminder_count)
            print("Reminders done")

            #weekly webinar info list---
            print("procedure-start8",datetime.now().time())
            Cursor.execute("set nocount on;exec SP_GetSeminarInfoCount")
            weekly_webinar=Cursor.fetchall() 
            if weekly_webinar:
                weekly_webinar=weekly_webinar[0]
                weekly_webinar=weekly_webinar[0]
            print("Weekly webinar=====",weekly_webinar)
            # weekly_webinar=len(weekly_webinar)            
            if(weekly_webinar < 9):
                weekly_webinar=str(weekly_webinar).zfill(2)
            #Live chat
            print("procedure-start9",datetime.now().time())
            date_to=datetime.today().date()
            # date_to=date_to.strftime("%Y-%m-%d")
            date_from=date_to-timedelta(days=date_to.weekday())
            print("date from---------------------------------------------------------",date_from)   
            print("date to---------------------------------------------------------",date_to)                   
            # Cursor.execute("set nocount on;exec SP_LiveChatLogSummary %s,%s,%s,%s",[date_from,date_to,'S',userId])
            # live_chat=Cursor.fetchone()
            Cursor.execute("set nocount on;exec SP_GetLiveChatCountWeekly_PY")
            live_chat=Cursor.fetchall()
            
            live_chat=len(live_chat)
            
            # if live_chat:
            #     live_chat=live_chat[0]
            # else:
            #     live_chat=0
            if(live_chat<9):
                live_chat=str(live_chat).zfill(2)
            print("Live chat=============================",live_chat)
            print("procedure-start10",datetime.now().time())
            
            Cursor.execute("set nocount on;exec SP_GetActiveCampaigns")
            active_campaigns=Cursor.fetchall()        
            
            active_campaigns_count=len(active_campaigns)
            
            for journel in journels:
                log_data=journel[0].split(":",1)  
                log_data[0]=log_data[0].strip()            
                journel_data.append((log_data[0],log_data[1],journel[3]))

            if all([(x[2]==0 and x[3]==0 and x[4]==0 and x[5]==0)for x in weekly_summary]):
                print("No weekly summary")
            else:
                for summary in  weekly_summary:
                    weekly_summary_bar.append({

                            'funded': summary[2],
                            'nonfunded':summary[3],
                            'temp':summary[4],
                            'waiting':summary[5],                      


                        })
            if all([(x[2]==0 and x[3] ==0) for x in leads_converted]):
                print("No leads converted")
            else:   
                for weekly_leads in leads_converted:
                    weekly_lead_bar.append({
                        'open':weekly_leads[2],
                        'closed':weekly_leads[3]
                    })

            print("procedure-end",datetime.now().time())
            sales_data={'weekly_summary':weekly_summary_bar,'ticket_count_daily':json.dumps(ticket_count_daily),'ticket_count_weekly':json.dumps(ticket_count_weekly),
            'journel':journel_data,'weekly_lead_bar':weekly_lead_bar,'meeting_today':meeting_today,'active_campaigns':active_campaigns,'campaign_count':active_campaigns_count,
            'live_chat':live_chat,'weekly_webinar':weekly_webinar,'reminders':reminders,'reminder_count':reminder_count,'reminder_count_show':reminder_count_show,
            'meeting_count':meeting_count,'due_week':due_week,'due_month':due_month}
            print("redirect start",datetime.now().time())
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return sales_data
    
    
    
    
    
    
    
    
    
    #----------------------------------------- Admin Dashboard ------------------------------------------------------------------
    
    def admin_dashboard(self,UserId):
        all_data={}
        
        meeting_daily_pie=[]
        meeting_weekly_pie=[]
        daily_live_bar=[]
        weekly_live_bar=[]
        status_bar=[]
        
        seminar_daily_pie=[]
        seminar_weekly_pie=[]
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
            Cursor=connection.cursor()
            Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[UserId])
            UserName=Cursor.fetchone()
            
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                date_yesterday=date_yesterday.strftime("%Y-%m-%d")

            print (date_yesterday)
            Cursor.execute("{call dbo.SP_GetDashboardCount(%s,%s,%s)}", [UserId,date_yesterday,date_today])
                
            result_set = Cursor.fetchall()        
        
            
            Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'w')           
            weekly_live_account = Cursor.fetchall()  
            
            Cursor.execute("set nocount on;exec SP_LiveAccountsCountByRepWeekly %s",'d')           
            livecount_daily = Cursor.fetchall()         
           
                     
           
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
          
            notification_count=notify_count[0]
            print("**************************",notification_count)            
           
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
            all_data={'username':UserName[0],'overview':result_set,'livecount_daily':json.dumps(livecount_daily),'leads':leads,
                        'live_account':live_account,'meeting_count':meetingcount,'spoken_call_one':spokencall_one,
                        'spoken_call':spokencall,'all_meetings':all_meetings,'meetingcount_daily':meetingcount_daily,
                        'seminarcount_daily':seminarcount_daily,'monthly_count':monthly_count,'active_users':active_users,
                        'seminarcount_weekly':seminarcount_weekly,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,
                        'weekly_live_account':weekly_live_bar,'daily_live_account':daily_live_bar,'leads_status':status_bar,'journels':journel,'active_campaigns':active_campaigns,'active_campaigns_count':active_campaigns_count,
                        'leads_pie':json.dumps(leads_pie),'halfyearly_bar':halfyearly_bar,'insta_followers':insta_follwers_list,'insta_count':count,
                        'notification':notification,'notification_count':notification_count}         
            
            
            
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)   
             
        finally:
            Cursor.close()

        return all_data
    
  
    #-------------------------------------------Manager Dashboard---------------------------------------------------------------------
    def manager_dashboard(self,userId):
        manager_data={}
        status_bar=[]
        meeting_daily_pie=[]
        meeting_weekly_pie=[]
        seminar_daily_pie=[]
        seminar_weekly_pie=[]
        halfyearly_bar=[]
        ticket_summary_bar=[]
        
        try:
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday_for_week = datetime.today()-timedelta(3)
                date_yesterday_for_today=datetime.today()-timedelta(3)
            else:
                date_yesterday_for_week = datetime.today()-timedelta(week_day)
                date_yesterday_for_today=datetime.today()-timedelta(1)

            date_yesterday_for_today=date_yesterday_for_today.strftime("%Y-%m-%d")
            date_yesterday_for_week=date_yesterday_for_week.strftime("%Y-%m-%d")
            one_week=datetime.today()-timedelta(days=7)
            one_week=one_week.strftime("%Y-%m-%d")
            # print("999999999999999999999999999999999999999999999",date_yesterday_for_today,date_today)
            # new_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[date_yesterday_for_today,date_today]).exclude(isib=1).values_list('login',flat=True))
            # print("New clients today=====",new_clients_today)
            # clients_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_today).values('accnt_no').annotate(Max('id'))
            # print("Clients today===",clients_today)
            # get_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_today.values('id__max')))
            # print("today id===",get_today_id)
            # disctinct_today_list=[]
            # for id in get_today_id.iterator():
            #     disctinct_today_list.append(id.id)
            # print("Distinct today list====",disctinct_today_list)
            # funded_today=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).count()
            # nonfunded_today=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).count()
            # print("New Funded Non Funded Today",funded_today,nonfunded_today)

            # new_clients_week=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[date_yesterday_for_week,date_today]).exclude(isib=1).values_list('login',flat=True))
            # clients_week=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_week).values('accnt_no').annotate(Max('id'))
            # get_week_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_week.values('id__max')))
            # disctinct_week_list=[]
            # for id in get_week_id.iterator():
            #     disctinct_week_list.append(id.id)

            # funded_week=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_week_list).count()
            # nonfunded_week=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_week_list).count()
            # print("New Funded Non Funded Week",funded_today,nonfunded_today,funded_week,nonfunded_week)


            # existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))
            # existing_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_today).values('accnt_no').annotate(Max('id'))
            # get_ext_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(existing_today.values('id__max')))
            # disctinct_ext_today_list=[]
            # for id in get_ext_today_id.iterator():
            #     disctinct_ext_today_list.append(id.id)


            # existing_funded_today=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday_for_today,date_today],id__in=disctinct_ext_today_list).count()
            
            # fu=list(TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status=1,trans_date__date__range=[date_yesterday_for_today,date_today],id__in=disctinct_ext_today_list))
            # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++fu",fu)
            # for i in fu:
            #     print("fufufuufu",i.accnt_no)
            # existing_nonfunded_today=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_ext_today_list).count()

            # print("Existing Funded Non Funded Today",funded_today,nonfunded_today,funded_week,nonfunded_week,existing_funded_today,existing_nonfunded_today)



            # existing_clients_week=list(TblClients.objects.filter(livestatus="Live",converteddate__date__gt=one_week).exclude(isib=1).values_list('login',flat=True))
           
            # all_existing=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))

            # total_existing=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_week).values('accnt_no').annotate(Max('id'))
            # get_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(total_existing.values('id__max')))
            # distinct_list=[]
           
            # for total in get_id.iterator():
            #     distinct_list.append(total.id)
            
            
            # total_all_existing=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=all_existing).values('accnt_no').annotate(Max('id'))
            # all_get_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(total_all_existing.values('id__max')))
            # all_distinct_list=[]
           
            # for total in all_get_id.iterator():
            #     all_distinct_list.append(total.id)
                

            # existing_funded_week=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday_for_week,date_today],id__in=distinct_list).count()
            
            # total_nonfun_existing=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=all_distinct_list).count()
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",["1990-09-19",date_today,"FundedLive"])
            exist_funded_today=Cursor.fetchone()
            if exist_funded_today:
                exist_funded_today=exist_funded_today[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",["1990-09-19",date_yesterday_for_week,"FundedLive"])
            exist_funded_week=Cursor.fetchone()
            if exist_funded_week:
                exist_funded_week=exist_funded_week[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",["1990-09-19",one_week,"NonFundedLive"])
            exist_nonfunded_week=Cursor.fetchone()
            if exist_nonfunded_week:
                exist_nonfunded_week=exist_nonfunded_week[0]
            
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_week,date_today])
            live_count=Cursor.fetchone()
            print("Live count this week======")
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_today,date_today])
            live_count_today=Cursor.fetchone()
            print("Live count======",live_count) 
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday_for_today,date_today,"FundedLive"])
            live_funded_today=Cursor.fetchone()
            if live_funded_today:
                live_funded_today=live_funded_today[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday_for_week,date_today,"FundedLive"])
            live_funded_week=Cursor.fetchone()
            if live_funded_week:
                live_funded_week=live_funded_week[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday_for_week,date_today,"NonFundedLive"])
            live_nonfund_week=Cursor.fetchone()
            if live_nonfund_week:
                live_nonfund_week=live_nonfund_week[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday_for_week,date_today,"TempApprovedPending"])
            pending_approved=Cursor.fetchone()
            if pending_approved:
                pending_approved=pending_approved[0]
            Cursor.execute("set nocount on;exec SP_GetNewAccountsListingCount %s,%s,%s",[date_yesterday_for_week,date_today,"WaitingApprovalPending"])
            pending_waiting=Cursor.fetchone()
            if pending_waiting:
                pending_waiting=pending_waiting[0]

            # if live_count_today:
                
            #     live_funded_today=live_count_today[0]
            #     live_nonfund_today=live_count_today[1]
            #     pending_approved=live_count_today[2]
            #     pending_waiting=live_count_today[3]
            # if live_count:
            #     live_funded_week=live_count[0]
            #     live_nonfund_week=live_count[1]
            Cursor.execute("set nocount on;exec SP_GetSeminarInfoCount")
            weekly_webinar=Cursor.fetchall() 
            if weekly_webinar:
                weekly_webinar=weekly_webinar[0]
                weekly_webinar=weekly_webinar[0]
            print("Weekly webinar=====",weekly_webinar)
            # weekly_webinar=len(weekly_webinar)            
            if(weekly_webinar < 9):
                weekly_webinar=str(weekly_webinar).zfill(2)
            Cursor.execute("set nocount on;exec SP_GetLiveChatCountWeekly_PY")
            live_chat=Cursor.fetchall()
            
            live_chat=len(live_chat)
            
            # if live_chat:
            #     live_chat=live_chat[0]
            # else:
            #     live_chat=0
            if(live_chat<9):
                live_chat=str(live_chat).zfill(2)
            Cursor.execute("set nocount on;exec SP_SpokenCallsCount")
            spokencall=Cursor.fetchall()
            Cursor.execute("set nocount on;exec SP_GetActiveCampaigns")
            active_campaigns=Cursor.fetchall()  
            active_campaigns_count=len(active_campaigns)
            print("Active campaing count=====",active_campaigns_count)
            Cursor.execute("exec SP_GetSummaryToday %s",[userId])
            reminders=Cursor.fetchall()  
            while (Cursor.nextset()):
                reminder_count = Cursor.fetchall()
                print("Reminder count-------",reminder_count)
                reminder_count=reminder_count[0]
                reminder_count=reminder_count[0]
            reminder_count=int(reminder_count)
            print("Reminder count====",reminder_count,type(reminder_count))

            if(reminder_count == 0):

                 reminder_count_show="00"
                 print("reminder count is zero")
            else:
                if(reminder_count < 9 ):
                    reminder_count_show=str(reminder_count)
                    reminder_count_show=reminder_count_show.zfill(2)
                else:
                    reminder_count_show=str(reminder_count)
            Cursor.execute("set nocount on;exec SP_GetLeadsStatusGraph")
            status_graph=Cursor.fetchall()
            print("Reminder count=====",reminder_count)
            Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'d')           
            meetingcount_daily = Cursor.fetchall()
            print("Meeting count daily==============",meetingcount_daily)
            Cursor.execute("set nocount on;exec SP_MeetingsCountByRepWeekly %s",'w')           
            meetingcount_weekly = Cursor.fetchall()
            
            Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'D')           
            seminarcount_daily = Cursor.fetchall()
            
            Cursor.execute("set nocount on;exec SP_SeminarsCountByRepWeekly %s",'W')           
            seminarcount_weekly = Cursor.fetchall()

            Cursor.execute("set nocount on;exec SP_GetHalfyearlySummary_PY")
            halfyearly_data=Cursor.fetchall()

            Cursor.execute("set nocount on;exec SP_GetMonthlyCount")
            monthly_summary=Cursor.fetchall()
            Cursor.execute("set nocount on;exec SP_TicketsInterestedSummary")
            ticket_summary=Cursor.fetchall()
            one_week=datetime.today()+timedelta(days=7)
            print("One week date===",one_week)
            two_week=datetime.today()-timedelta(days=14)
            print("Two week=====",two_week)
            due_tickets=TblActionreasons.objects.filter(duedate__lt=one_week,duedate__gt=two_week).values()
            print("due tickets**************************************************",due_tickets)
            print("Type of ticket summary===",type(ticket_summary))
            if ticket_summary:
                last_item=ticket_summary[-1:][0]
                last_data=last_item[-1]
                print("Last Item =====",last_data)
                for tickets in ticket_summary[:-1]:
                    print("Tickets===1",tickets[1])
                    print("Tickets===2",tickets[2])
                    percent=(tickets[1]/last_data)*100
                    percent=round(percent,2)
                    ticket_summary_bar.append({
                        'name': tickets[0],
                        'percent':percent
                    })

            print("Ticket summary bar=====",ticket_summary_bar)
            for data in halfyearly_data:
                halfyearly_bar.append({

                        'month': data[1],
                        'live_account':data[3],
                        'pending_account':data[4],
                        'funded_account':data[5],
                        'tickets':data[6],
                        'leads':data[7]


                    })  

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

            for status in status_graph:
                status_bar.append({
                        'name': status[0],
                        'src_count':status[1],
                        'ticket_count':status[2]


                    })
          
            manager_data={'funded_today':live_funded_today,'funded_week':live_funded_week,'nonfunded_week':live_nonfund_week,'webinars':weekly_webinar,'livechat':live_chat,'calls':spokencall,'campaigns':active_campaigns,'reminders':reminders,
                           'approved':pending_approved,'waiting':pending_waiting,'summary':monthly_summary,'ticket_summary':ticket_summary_bar,'remindercount':reminder_count,'reminder_count_show':reminder_count_show,'campaign_count':active_campaigns_count,
                           'leads_graph':status_bar,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'halfyearly_bar':halfyearly_bar,'dues':due_tickets,
                           'new_fund_today':live_funded_today,'new_fund_week':live_funded_week,'new_nonfund_week':live_nonfund_week,'ext_fund_today':exist_funded_today,'ext_nonfund_today':exist_funded_week,'ext_fund_week':exist_funded_today,
                           'total_nonfun':exist_nonfunded_week
                           
                           }  
                        #    'new_fund_today':funded_today,'new_nonfund_today':nonfunded_today,'new_fund_week':funded_week,'new_nonfund_week':nonfunded_week,  
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__,e)   
             
        finally:
            Cursor.close()
        return manager_data

    # ======================Back office dashboard========
    #Dashboard data
    def backoffice_dashboard(self,userId):
        print("Backoffice user id=====",userId)
        dash_data={}
        try:
            Cursor=connection.cursor()           
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday_for_week = datetime.today()-timedelta(3)
                date_yesterday_for_today=datetime.today()-timedelta(3)
            else:
                date_yesterday_for_week = datetime.today()-timedelta(week_day)
                date_yesterday_for_today=datetime.today()-timedelta(1)

            date_yesterday_for_today=date_yesterday_for_today.strftime("%Y-%m-%d")
            date_yesterday_for_week=date_yesterday_for_week.strftime("%Y-%m-%d")
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_week,date_today])
            live_count=Cursor.fetchone()
            print("Live count this week======")
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_today,date_today])
            live_count_today=Cursor.fetchone()
            
            if live_count_today:
                
                live_funded_today=live_count_today[0]
                live_nonfund_today=live_count_today[1]
                pending_approved=live_count_today[2]
                pending_waiting=live_count_today[3]
            if live_count:
                live_funded_week=live_count[0]
                live_nonfund_week=live_count[1]
            Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[userId])
            journels=Cursor.fetchall()
            Cursor.execute("set nocount on;exec SP_GetPendingCryptoApproval_PY")
            pending_crypto=Cursor.fetchall() 
            pending_crypto_count=len(pending_crypto)
            Cursor.execute("set nocount on;exec SP_GetPendingCreditCardApproval_PY")
            pending_credit=Cursor.fetchall() 
            pending_credit_count=len(pending_credit)
            Cursor.execute("set nocount on;exec SP_GetExpiryDocs")
            missing_docs=Cursor.fetchall() 
            missing_docs_count=len(missing_docs)
            Cursor.execute("set nocount on;exec SP_GetEWalletTransHistory %s,%s,%s",[date_yesterday_for_today,date_today,4])
            pending_trans=Cursor.fetchall() 
            dash_data={'funded_today':live_funded_today,'nonfunded_today':live_nonfund_today,'funded_week':live_funded_week,'nonfunded_week':live_nonfund_week,
            'approved':pending_approved,'waiting':pending_waiting,'journel':journels,'pending_crypto':pending_crypto,'pending_crypto_count':pending_crypto_count,
            'pending_credit':pending_credit,'pending_credit_count':pending_credit_count,'missing_docs':missing_docs,'missing_docs_count':missing_docs_count,
            'pending_trans':pending_trans}
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return dash_data
#Complaint dashboard======
    def complaint_dashboard(self,userId):
        dash_data={}
        try:
            Cursor=connection.cursor()           
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday_for_week = datetime.today()-timedelta(3)
                date_yesterday_for_today=datetime.today()-timedelta(3)
            else:
                date_yesterday_for_week = datetime.today()-timedelta(week_day)
                date_yesterday_for_today=datetime.today()-timedelta(1)

            date_yesterday_for_today=date_yesterday_for_today.strftime("%Y-%m-%d")
            date_yesterday_for_week=date_yesterday_for_week.strftime("%Y-%m-%d")
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_week,date_today])
            live_count=Cursor.fetchone()
            print("Live count this week======")
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_today,date_today])
            live_count_today=Cursor.fetchone()
            
            if live_count_today:
                
                live_funded_today=live_count_today[0]
                live_nonfund_today=live_count_today[1]
                pending_approved=live_count_today[2]
                pending_waiting=live_count_today[3]
            if live_count:
                live_funded_week=live_count[0]
                live_nonfund_week=live_count[1]
            Cursor.execute("set nocount on;exec SP_GetComplaintsList %s",[21])
            complaints=Cursor.fetchall()
            complaints_count=len(complaints)
            print("Complaints====",complaints)
            dash_data={'funded_today':live_funded_today,'nonfunded_today':live_nonfund_today,'funded_week':live_funded_week,'nonfunded_week':live_nonfund_week,
            'approved':pending_approved,'waiting':pending_waiting,'complaints':complaints,'count':complaints_count}
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return dash_data






