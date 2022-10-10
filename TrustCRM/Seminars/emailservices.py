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
            print("Deatils======================",repname,username,ticket,salesrepid)
            Cursor.execute("SELECT Email FROM tbl_User where UserID=%s",[salesrepid])
            receiver_mail=Cursor.fetchone()
            print("Receiver mail-----------------------------",receiver_mail)
            subject="SalesRep Assigned"   
            email_from = 'cs@trusttc.com'
            
            template_data={
                "repname":repname,
                "username":username,
                "ticket":ticket

            }
            print("Templatedata=====",template_data)
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
            
            # receiver_mail="aswani.technology@gmail.com"
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
    def send_email_templates(self,lang,subject,receiver_mail,title,name,salesrep):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------")   
            
            print("Receiver mail-----------------------------",receiver_mail)
            # bcc='crm@trusttc.com'
            title=" "
            fromaddr="cs@trusttc.com"
            
            template_data={
                "title":title,
                "name":name, 
                "rep":salesrep             

            }
            if(subject=="About Trust Capital"):
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
            if(subject=="Trust Capital - Missing POR"):
                if(lang=="en"):
                    path="email/EN/MissingProofofResidence.html"
                if(lang=="ch"):
                    path="email/CH/MissingProofofResidence.html"
            if(subject=="Trust Capital Limited - Missing ID"):
                if(lang=="en"):
                    path="email/EN/MissingId.html"
                if(lang=="ch"):
                    path="email/CH/MissingId.html"
            
            
            
            
                
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=fromaddr,to=[receiver_mail])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------",e)    
        finally:
            pass

    
    def send_mail_manageTicket(self,to,sub,emailbody):
        try:
               
            print("Email service---------------------------------------")             
            
           
            email_from = 'crm@trusttc.com'
           
            print("Receiver mail-----------------------------",to,sub,emailbody)
            email_template_render=emailbody
            msg = EmailMultiAlternatives(subject=sub,from_email=email_from,to=[to])
            msg.attach_alternative(email_template_render, "text/html")

            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
                pass

    #open demo account email
    def demo_account_email(self,title,name,demo_account,password,receiver_mail):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------")   
            bcc1="crm@trusttc.com"
            bcc2="cs@trusttc.com"
            
           
            email_from = 'cs@trusttc.com'
            # receiver_mail="aswani.technology@gmail.com"
            template_data={
                "title":title,
                "name":name,
                "login":demo_account,
                "password":password,
            }
            email_template_render=render_to_string("email/YourDemoAccountWithTrustCapital.html",template_data)
            subject="Your Demo Account With Trust Capital"
            
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver_mail],bcc=[bcc1])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")   
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
                pass

    #seminar confirmation email
    def seminar_confirmation_email(self,title,name,to_addr,seminartitle):
        try:
            
            subject = "Trust Capital - Webinar Confirmation"
            from_addr="crm@trusttc.com"
            bcc="crm@trusttc.com"
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_SeminarConfirmationEmail %s",[seminartitle]) 
            seminar_details=Cursor.fetchone()
            title=" "
            if seminar_details:
                seminar_name=seminar_details[2]
                location=seminar_details[0]
                seminar_date=seminar_details[1]
                seminar_time=seminar_details[3]
            template_data={
                "title":title,
                "name":name,
                "seminar_name":seminar_name,
                "location":location,
                "seminar_date":seminar_date,
                "seminar_time":seminar_time

            }
            
            email_template_render=render_to_string("email/SendSeminar.html",template_data)
            
            msg = EmailMultiAlternatives(subject=subject,from_email=from_addr,to=[to_addr],bcc=[bcc])
            
            msg.attach_alternative(email_template_render, "text/html")
            
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
            Cursor.close()        

  #Account update email
    def account_update_email(self,accountno,ticket,request,update_result):
        try:
            subject = "Updated Account "+accountno
            # from_addr="crm@trusttc.com"
            from_addr="crm@trusttc.com"
            bcc="backoffice@trusttc.com"
            to_addr="compliance@trusttc.com"
            # to_addr="aswani.technology@gmail.com"
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetEmailDetails %s",[accountno]) 
            account_details=Cursor.fetchone()
            Cursor.execute("set nocount on;exec SP_GetTicket_PY %s",[ticket])
            client_details=Cursor.fetchone()
            # name=request.POST.get('firstname')
            # email=request.POST.get('email')
            # phone=request.POST.get('phone')
            # sub=request.POST.get('subject')
            # profession=request.POST.get('profession')
            # dob=request.POST.get('dob')
            # age=request.POST.get('age')
            # address=request.POST.get('address')
            # country=request.POST.get('country')
            # if client_details:
            #     sender=client_details[3]
            sender=request.session.get('Email')
           
            template_data={
              "accountno":accountno,
              "sender":sender,
              "updateinfo":update_result
            }
            email_template_render=render_to_string("email/UpdatedAccount.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=from_addr,to=[to_addr],bcc=[bcc])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")
        except Exception as e:
                print("EXCEPTION-----------------------")    
        finally:
            Cursor.close()    




       
       
