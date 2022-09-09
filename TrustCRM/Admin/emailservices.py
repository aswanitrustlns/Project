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

    #send email templates
    def send_email_templates(self,lang,subject,fromaddr,receiver_mail,title,name):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------")   
            
            print("Receiver mail-----------------------------",receiver_mail)
            # bcc='crm@trusttc.com'
            bcc='aswani@trustlns.ae'
            
            receiver_mail="aswani.technology@gmail.com"
            template_data={
                "title":title,
                "name":name,              

            }
            if(subject=="About TC Limited"):
                if(lang=="en"):
                    path="email/EN/AboutTrustCapitalTC.html"
                if(lang=="ch"):
                    path="email/CH/AboutTrustCapitalTC.html"
            if(subject=="How To open an Account"):
                if(lang=="en"):
                    path="email/EN/HowToOpenAnAccount.html"
                if(lang=="ch"):
                    path="email/CH/HowToOpenAnAccount.html"
            if(subject=="Rejection Of Application"):
                if(lang=="en"):
                    path="email/EN/RejectionofApplication.html"
                if(lang=="ch"):
                    path="email/CH/RejectionofApplication.html"
            if(subject=="Webinar Registration"):
                if(lang=="en"):
                    path="email/EN/WebinarRegistration.html"
                if(lang=="ch"):
                    path="email/CH/WebinarRegistration.html"
            if(subject=="POR And POI"):
                if(lang=="en"):
                    path="email/EN/PORAndPOI.html"
                if(lang=="ch"):
                    path="email/CH/PORAndPOI.html"
            if(subject=="Unreachable"):
                if(lang=="en"):
                    path="email/EN/unreachable.html"
                if(lang=="ch"):
                    path="email/CH/unreachable.html"
            if(subject=="MetaTrader 4 Advantages"):
                if(lang=="en"):
                    path="email/EN/MetaTrader4Advantages.html"
                if(lang=="ch"):
                    path="email/CH/MetaTrader4Advantages.html"
            if(subject=="Mobile Trading"):
                if(lang=="en"):
                    path="email/EN/MobileTrading.html"
                if(lang=="ch"):
                    path="email/CH/MobileTrading.html"
            if(subject=="Trading Instruments"):
                if(lang=="en"):
                    path="email/EN/TradingInstruments.html"
                if(lang=="ch"):
                    path="email/CH/TradingInstruments.html"
            if(subject=="Unreachable SMS"):
                if(lang=="en"):
                    path="email/EN/UnreachSMS_EN.html"
                if(lang=="ch"):
                    path="email/CH/UnreachSMS_CH.html"
            if(subject=="Sales Call Interested SMS"):
                if(lang=="en"):
                    path="email/EN/Interested_CH.html"
                if(lang=="ch"):
                    path="email/CH/Interested_EN.html"
            if(subject=="TC Limited - Missing POR"):
                if(lang=="en"):
                    path="email/EN/MissingProofofResidence.html"
                if(lang=="ch"):
                    path="email/CH/MissingProofofResidence.html"
            if(subject=="TC Limited - Missing ID"):
                if(lang=="en"):
                    path="email/EN/MissingId.html"
                if(lang=="ch"):
                    path="email/CH/MissingId.html"
            
            
            
            
                
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=fromaddr,to=[receiver_mail],bcc=[bcc])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
            pass

    
    def send_mail_manageTicket(self,fromaddr,to,name,title,sub,emailbody):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------")   
            
            print("Receiver mail-----------------------------",receiver_mail)
            subject="SalesRep Assigned"   
            email_from = 'cs@trusttc.com'
            receiver_mail="aswani.technology@gmail.com"
            
            email_template_render=render_to_string("email/NewSalesInquiryReAssigned.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver_mail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
                pass

       
       
