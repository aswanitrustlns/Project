import time

from .models import TblClients,TblSaleslead,TblUser,TblEwalletTransaction,TblTicketlogs
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', id="my_job_id", seconds=3600)
def test():
    one_month_ago = datetime.today() - timedelta(days=30)
    one_week=datetime.today()-timedelta(days=20)
    two_week=datetime.today()-timedelta(days=30)
    print("One week====",one_week)
    print("One month age===",one_month_ago)
    nonfunded_in_week=TblClients.objects.filter(regdate__gte=one_week,livestatus="Live").values()
    
    nonfunded_second_week=TblClients.objects.filter(regdate__range=(one_week,two_week),livestatus="Live").values()
    
    if nonfunded_in_week:
        for non in nonfunded_in_week.iterator():
            login=non["login"]
            print("Login=====",login)
            pending_first=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0)#filter trans_status=0
            if pending_first:
                for data in pending_first.iterator():
                    pass #send mail to salesrep

    if nonfunded_second_week:                   
        print("Non funded second week=====",nonfunded_second_week)
        for data in nonfunded_second_week.iterator():
            ticket=data["login"]
            pending_first=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0)#filter trans_status=0
            reason_check=TblTicketlogs.objects.filter(ticket=ticket,chattype="Nonfunded Reason")
            if reason_check:
                print("reason entered======== give one more month")
            print("Second week ",data["login"])

   
        # print("Login====",login)
        # ticket=non["ticket"]
        # pending=TblEwalletTransaction.objects.using('svg').filter(accnt_no="404005")
        # for data in pending.iterator():

        #     print("pending",data.accnt_no)
    print("Working===")
   

scheduler.start()