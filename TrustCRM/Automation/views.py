import time
from .models import TblClients,TblSaleslead,TblUser,TblEwalletTransaction,TblTicketlogs
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from emailservice import EmailServices
scheduler = BackgroundScheduler()
emailservices=EmailServices()

@scheduler.scheduled_job('interval', id="my_job_id", seconds=25)
def test():
    ticket=""
    one_month_ago = datetime.today() - timedelta(days=30)
    one_week=datetime.today()-timedelta(days=85)
    two_week=datetime.today()-timedelta(days=14)
    print("One week====",one_week)
    print("One month age===",one_month_ago)
    nonfunded_in_week=TblClients.objects.filter(regdate__gte=one_week,livestatus="Live").values()
    
    nonfunded_second_week=TblClients.objects.filter(regdate__range=(one_week,two_week),livestatus="Live").values()
    
    if nonfunded_in_week:
        for non in nonfunded_in_week.iterator():
            login=non["login"]
            ticket=non["ticket"]
            print("Login=====",login)
            pending_first=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0,trans_type=0).values_list('accnt_no').distinct()#filter trans_status=0
            # print("Pending first week",pending_first,type(pending_first))
            if pending_first:
                
                for data in pending_first.iterator():
                    print("pending first weekkk",data[0])
                    emailservices.mail_after_one_week(ticket)

    print("Non funded second week======")
    if nonfunded_second_week:                   
        
        for data in nonfunded_second_week.iterator():
           
            pending_second=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0,trans_type=0).values_list('accnt_no').distinct()#filter trans_status=0
            if pending_second:
                print("Pending first=====")
                for data in pending_second.iterator():
                    ticket=data.ticket
                    reason_check=TblTicketlogs.objects.filter(ticket=ticket,chattype="Nonfunded Reason")
                    print("Reason check",reason_check)
           

   
        # print("Login====",login)
        # ticket=non["ticket"]
        # pending=TblEwalletTransaction.objects.using('svg').filter(accnt_no="404005")
        # for data in pending.iterator():

        #     print("pending",data.accnt_no)
    print("Working===")
   

scheduler.start()