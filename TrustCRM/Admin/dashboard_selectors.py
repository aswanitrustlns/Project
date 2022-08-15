from django.db import connection
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
            
            Cursor.execute("set nocount on;exec SP_SalesTicketCountByRepWeekly %s,%s",['W',userId])
            ticket_count_weekly=Cursor.fetchone()
            
            Cursor.execute("set nocount on;exec SP_GetActivityLogsDB %s",[userId])
            journels=Cursor.fetchall()

            
            Cursor.execute("set nocount on;exec SP_GetWeeklyLeads_PY")
            leads_converted=Cursor.fetchall()

            for journel in journels:
                log_data=journel[0].split(":",1)                
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

            print("Ticket count daily-----",ticket_count_daily)
            sales_data={'weekly_summary':weekly_summary_bar,'ticket_count_daily':json.dumps(ticket_count_daily),'ticket_count_weekly':json.dumps(ticket_count_weekly),'journel':journel_data,'weekly_lead_bar':weekly_lead_bar}
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return sales_data
