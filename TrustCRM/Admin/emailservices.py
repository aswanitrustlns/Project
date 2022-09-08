from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import BadHeaderError
from django.template.loader import render_to_string
from django.db import connection

class EmailServices:

    def send_SalesInquiry_Assigned(self,repname,username,ticket,salesrepid):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------")   
            Cursor=connection.cursor()
            Cursor.execute("SELECT Email FROM tbl_User where UserID=%s",[salesrepid])
            receiver_mail=Cursor.fetchone()
            print("Receiver mail-----------------------------",receiver_mail)
            subject="SalesRep Assigned"   
            email_from = 'cs@trusttc.com'
            receiver_mail="aswani.technology@gmail.com"
            template_data={
                "repname":repname,
                "username":username,
                "ticket":ticket

            }
            email_template_render=render_to_string("email/NewSalesInquiryAssigned.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver_mail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
            Cursor.close()  

    def send_SalesInquiry_Reassigned(self,repname,username,ticket,salesrepid):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------")   
            Cursor=connection.cursor()
            Cursor.execute("SELECT Email FROM tbl_User where UserID=%s",[salesrepid])
            receiver_mail=Cursor.fetchone()
            print("Receiver mail-----------------------------",receiver_mail)
            subject="SalesRep Assigned"   
            email_from = 'cs@trusttc.com'
            receiver_mail="aswani.technology@gmail.com"
            template_data={
                "repname":repname,
                "username":username,
                "ticket":ticket

            }
            email_template_render=render_to_string("email/NewSalesInquiryReAssigned.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver_mail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
            Cursor.close()   
       
       
