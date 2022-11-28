from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import BadHeaderError
from django.template.loader import render_to_string
from django.db import connection
from .models import TblSaleslead,TblUser

class EmailServices:
    def mail_after_one_week(self,ticket):
        repid=""
        repname=""
        repemail=""
        salesrep=TblSaleslead.objects.filter(ticket_no=ticket)
        for rep in salesrep.iterator():
            repid=rep["salesrepid"]
        if repid!="":
            repdetails=TblUser.objects.filter(userid=repid)
            for details in repdetails.iterator():
                repname=details["username"]
                repemail=details["email"]
        if(repemail!=""):
            subject="Attention Please"   
            email_from = 'cs@trusttc.com'
            message="Your account "+ticket+" was not funded"
            template_data={
                "repname":repname,
                "ticket":ticket,
                "message":message,

            } 
            email_template_render=render_to_string("email/Notification.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[repemail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)  

    def reassign_to_manager(self,ticket):
        repid=""
        repname=""
        repemail=""
        salesrep=TblSaleslead.objects.filter(ticket_no=ticket)
        for rep in salesrep.iterator():
            repid=rep["salesrepid"]
        if repid!="":
            repdetails=TblUser.objects.filter(userid=repid)
            for details in repdetails.iterator():
                repname=details["username"]
                repemail=details["email"]
        if(repemail!=""):
            subject="Attention Please"   
            email_from = 'cs@trusttc.com'
            message="Your account "+ticket+" was not funded"
            template_data={
                "repname":repname,
                "ticket":ticket,
                "message":message
            } 
            email_template_render=render_to_string("email/Notification.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[repemail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)

         

