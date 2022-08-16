from django.db import connection
from datetime import datetime, timedelta
import json
class DashboardSelector:

    def sales_dashboard(self,userId):
        userId=56
        sales_data={}
        weekly_summary_bar=[]
        journel_data=[]
        weekly_lead_bar=[]
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetWeeklySummary_PY  %s",[userId])
            weekly_summary=Cursor.fetchall()
            print("--------------------------------------------------------------------------------")
            Cursor.execute("set nocount on;exec SP_SalesTicketCountByRepWeekly %s,%s",['D',userId])
            ticket_count_daily=Cursor.fetchone()
            print("ticket count daily-----------------------",type(ticket_count_daily))    
            # if all([(x[1]==0 and x[2]==0 and x[3]==0)for x in ticket_count_daily]):
            #     ticket_count_daily=[]
            
            Cursor.execute("set nocount on;exec SP_SalesTicketCountByRepWeekly %s,%s",['W',userId])
            ticket_count_weekly=Cursor.fetchone()
            print("ticket count daily-----------------------",type(ticket_count_weekly))    
            # if all([(x[1]==0 and x[2]==0 and x[3]==0)for x in ticket_count_weekly]):
            #     ticket_count_weekly=[]
            
            Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[userId])
            journels=Cursor.fetchall()
                        
            Cursor.execute("set nocount on;exec SP_GetWeeklyLeads_PY")
            leads_converted=Cursor.fetchall()  
            #Meetingsss
            Cursor.execute("set nocount on;exec SP_GetMeetings")
            meeting_today=Cursor.fetchall() 
              
            #Reminders....
            Cursor.execute("set nocount on;exec SP_GetSummaryToday %s",[userId])
            reminders=Cursor.fetchall()
            print("Reminders---------------------------------",reminders)
            #weekly webinar info list---
            Cursor.execute("set nocount on;exec SP_GetSeminarInfolist")
            weekly_webinar=Cursor.fetchall() 
           
            #Live chat
            date_to=datetime.today().date()
            # date_to=date_to.strftime("%Y-%m-%d")
            date_from=date_to-timedelta(days=date_to.weekday())
            print("date from---------------------------------------------------------",date_from)   
            print("date from---------------------------------------------------------",date_to)                   
            Cursor.execute("set nocount on;exec SP_LiveChatLogSummary %s,%s,%s,%s",[date_from,date_to,'S',userId])
            live_chat=Cursor.fetchone()
            if live_chat:
                live_chat=live_chat[0]
            else:
                live_chat=0
            print("Live chat=============================",live_chat)
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

           
            sales_data={'weekly_summary':weekly_summary_bar,'ticket_count_daily':json.dumps(ticket_count_daily),'ticket_count_weekly':json.dumps(ticket_count_weekly),
            'journel':journel_data,'weekly_lead_bar':weekly_lead_bar,'meeting_today':meeting_today,'active_campaigns':active_campaigns,'campaign_count':active_campaigns_count,
            'live_chat':live_chat,'weekly_webinar':weekly_webinar}
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return sales_data
