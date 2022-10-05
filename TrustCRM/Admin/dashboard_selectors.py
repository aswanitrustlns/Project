from django.db import connection
from datetime import datetime, timedelta
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
            'live_chat':live_chat,'weekly_webinar':weekly_webinar,'reminders':reminders,'reminder_count':reminder_count,'reminder_count_show':reminder_count_show,'meeting_count':meeting_count}
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
            print("Date yesterday========================",date_yesterday_for_week)
            print("Date yesterday========================",date_yesterday_for_today)
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_week,date_today])
            live_count=Cursor.fetchone()
            print("Live count this week======")
            Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[date_yesterday_for_today,date_today])
            live_count_today=Cursor.fetchone()
            print("Live count======",live_count)
            if live_count:
                
                live_funded_week=live_count[0]
                live_nonfund_week=live_count[1]
                pending_approved=live_count[2]
                pending_waiting=live_count[3]
            if live_count_today:
                live_funded_today=live_count_today[0]
                live_nonfund_today=live_count_today[1]
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
            Cursor.execute("exec SP_GetSummaryToday %s",[userId])
            reminders=Cursor.fetchall()  
            while (Cursor.nextset()):
                reminder_count = Cursor.fetchall()
                print("Reminder count-------",reminder_count)
                reminder_count=reminder_count[0]
                reminder_count=reminder_count[0]
            print("Reminder count-------",type(reminder_count))
            reminder_count=int(reminder_count)
            print("Reminder count=======",reminder_count)
            Cursor.execute("set nocount on;exec SP_GetLeadsStatusGraph")
            status_graph=Cursor.fetchall()

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

            if ticket_summary:
                for tickets in ticket_summary:
                    percent=(tickets[1]/tickets[2])*100
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
          
            manager_data={'funded_today':live_funded_today,'nonfunded_today':live_nonfund_today,'funded_week':live_funded_week,'nonfunded_week':live_nonfund_week,'webinars':weekly_webinar,'livechat':live_chat,'calls':spokencall,'campaigns':active_campaigns,'reminders':reminders,
                           'approved':pending_approved,'waiting':pending_waiting,'summary':monthly_summary,'ticket_summary':ticket_summary_bar,'remindercount':reminder_count,
                           'leads_graph':status_bar,'meeting_daily_pie': meeting_daily_pie,'meeting_weekly_pie':meeting_weekly_pie,'seminar_weekly_pie': seminar_weekly_pie,'seminar_daily_pie':seminar_daily_pie,'halfyearly_bar':halfyearly_bar}    
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!!!!!!!!!",e.__class__)   
             
        finally:
            Cursor.close()
        return manager_data





