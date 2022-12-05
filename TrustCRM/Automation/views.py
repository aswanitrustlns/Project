# import time
# from .models import TblClients,TblSaleslead,TblUser,TblEwalletTransaction,TblTicketlogs
# from datetime import datetime, timedelta
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from .emailservice import EmailServices
# scheduler = BackgroundScheduler()
# emailservices=EmailServices()

# @scheduler.scheduled_job(id="my_job_id",trigger='cron', hour='10', minute='30')
# def test():
#     ticket=""
#     one_month_ago = datetime.today() - timedelta(days=30)
#     one_week=datetime.today()-timedelta(days=7)
#     two_week=datetime.today()-timedelta(days=14)
#     third_week=datetime.today()-timedelta(days=21)
#     print("One week====",one_week)
#     print("One month age===",one_month_ago)
#     nonfunded_in_week=TblClients.objects.filter(regdate__gte=one_week,livestatus="Live").values()
    
#     nonfunded_second_week=TblClients.objects.filter(regdate__range=(one_week,two_week),livestatus="Live").values()
#     nonfunded_third_week=TblClients.objects.filter(regdate__range=(two_week,third_week),livestatus="Lve").values()
#     managerid=TblUser.objects.filter(username="online").only('userid').first()
#     print("Manager id--------",managerid.userid)
#     if nonfunded_in_week:
#         for non in nonfunded_in_week.iterator():
#             login=non["login"]
#             ticket=non["ticket"]
#             print("Login=====",login)
#             pending_first=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0,trans_type=0).values_list('accnt_no').distinct()#filter trans_status=0
#             # print("Pending first week",pending_first,type(pending_first))
#             if pending_first:
                
#                 for data in pending_first.iterator():
#                     print("pending first weekkk",data[0])
#                     emailservices.mail_after_one_week(ticket)

#     if nonfunded_second_week:                   
#         for data in nonfunded_second_week.iterator():
#             pending_second=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0,trans_type=0).values_list('accnt_no').distinct()#filter trans_status=0
#             if pending_second:
#                 print("Pending first=====")
#                 for data in pending_second.iterator():
#                     ticket=data.ticket
#                     reason_check=TblTicketlogs.objects.filter(ticket=ticket).only("chattype").first()
#                     print("Reason check",reason_check.chattype)
#                     if(reason_check.chattype=="Nonfunded Reason"):
#                         emailservices.mail_after_one_week(ticket)
#                     else:
#                         reassignticket=TblSaleslead.objects.get(ticket_no=ticket)
#                         reassignticket.salesrepid=managerid
#                         reassignticket.save()
#                         emailservices.reassign_to_manager(ticket) 

#     if nonfunded_third_week:
#         for data in nonfunded_second_week.iterator():
#             pending_third=TblEwalletTransaction.objects.using('svg').filter(accnt_no=login,trans_status=0,trans_type=0).values_list('accnt_no').distinct()#filter trans_status=0
#             if pending_third:
#                 print("Pending first=====")
#                 for data in pending_third.iterator():
#                     ticket=data.ticket
#                     reassignticket=TblSaleslead.objects.get(ticket_no=ticket)
#                     reassignticket.salesrepid=managerid
#                     reassignticket.save()
#                     emailservices.reassign_to_manager(ticket)
   
#         # print("Login====",login)
#         # ticket=non["ticket"]
#         # pending=TblEwalletTransaction.objects.using('svg').filter(accnt_no="404005")
#         # for data in pending.iterator():

#         #     print("pending",data.accnt_no)
#     print("Working===")
   

# scheduler.start()