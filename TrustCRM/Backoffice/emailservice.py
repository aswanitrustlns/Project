from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import BadHeaderError
from django.template.loader import render_to_string
from django.db import connection
class EmailServices:
    def change_password_notification(self,login):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------",login)   
            
        
            subject="Account Passwords Notification"   
            email_from = 'cs@trusttc.com'
            bcc_mail="crm@trusttc.com"
            cc_mail="magt@trusttc.com"
            receiver_mail="backoffice@trusttc.com"
            template_data={
                "login":login
            }
            print("Templatedata=====",template_data)
            email_template_render=render_to_string("email/PasswordChangeNotificationTC.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver_mail],bcc=[bcc_mail],cc=[cc_mail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
            print("EXCEPTION-----------------------")  

    def password_reset_info(self,masterPwd,investorPwd,phonePwd,login):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetEmailDetails %s",[login]) 
            account_details=Cursor.fetchone()
            if account_details:
                name=account_details[1]
                title=account_details[3]
                receiver_mail=account_details[0]
            template_data={
                "title":title,
                "name":name,
                "MPassword":masterPwd,
                "IPassword":investorPwd,
                "PPassword":phonePwd
            }  
            subject="Account Passwords"
            email_from = 'cs@trusttc.com'
            bcc_mail="crm@trusttc.com"
            email_template_render=render_to_string("email/PasswordResetInfofromTrustCapitalTC.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver_mail],bcc=[bcc_mail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
           
        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close()
       