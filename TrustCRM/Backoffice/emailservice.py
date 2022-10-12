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
    #Rejection of account
    def rejectionofaccount(self,title,name,remail,salesrep,reason):
        try:
            Cursor=connection.cursor()  
            subject = "Account Rejected - Trust Capital"
            email_from = 'cs@trusttc.com'
            bcc1="crm@trusttc.com"
            bcc2="backoffice@trusttc.com"
            template_data={
                "title":title,
                "name":name,
                "salesrep":salesrep
            }  

            if (reason == 24):
                path = "email/backoffice/RejectionofAccountBelgium.html"
            elif (reason == 25):
                path = "email/backoffice/RejectionofAccountThirdCountry.html"
            elif (reason == 26):
                path = "email/backoffice/RejectionofAccountVulnerable.html"
            elif (reason == 27):
                path = "email/backoffice/RejectionofAccountApprpriatenessTest.html"
            else: 
                path = "email/backoffice/RejectionofAccountGeneric.html"
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close()  

    #send termination of account
    def terminationofaccount(self,title,name,remail,reason):
        try:
            Cursor=connection.cursor()  
            subject = "Account Terminated - Trust Capital"
            email_from = 'cs@trusttc.com'
            bcc1="crm@trusttc.com"
            bcc2="backoffice@trusttc.com"
            bcc3="compliance@trusttc.com"
            bcc4="magt@trusttc.com"
            template_data={
                "title":title,
                "name":name,
                
            }  

            if (reason == 28):
                path = "email/backoffice/TerminationofAccountApprVulnerable.html"
            elif (reason == 29):
                path = "email/backoffice/TerminationofAccountApprVulnerableRemBalance.html"
            elif (reason == 30 or reason==34):
                path = "email/backoffice/TerminationofAccountAMLKYCDoc.html"
            else: 
                path = "email/backoffice/TerminationofAccountAMLKYCDocGeneric.html"
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close()  
    #Send Temperory Account Details
    def SendTempAccountDetails(self,title,name,remail,accno,acctype):
        try:
            Cursor=connection.cursor()  
            subject = "Your Live Trust Capital Account Details"
            email_from = 'cs@trusttc.com'
            bcc1="crm@trusttc.com"
            bcc2="backoffice@trusttc.com"
            bcc3="compliance@trusttc.com"
            bcc4="magt@trusttc.com"
            template_data={
                "title":title,
                "name":name,
                "acctype":acctype,
                "account":accno
                
            }  
            email_template_render=render_to_string("email/backoffice/TempAccountDetails.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

     #Card approval
    def SendCardApprovalmail(self,title,name,remail,cardno,cardtype,status):
        try:
            Cursor=connection.cursor()  
            subject=""
           
                
            email_from = 'cs@trusttc.com'
            print("Mail======",title,name,remail,cardno,subject)
            # bcc1="crm@trusttc.com"
            # bcc2="backoffice@trusttc.com"
            # bcc3="compliance@trusttc.com"
            # bcc4="magt@trusttc.com"
            remail="aswani.technology@gmail.com"
            template_data={
                "title":title,
                "name":name,
                "cardno":cardno
                
            }  
            if (status=="Approved"):
                subject = "Credit Card Approved"
                path="email/backoffice/CreditCardApproved.html"
            if(status=="Rejected"):
                subject = "Credit Card Rejected"
                path="email/backoffice/CreditCardRejected.html"
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail])#bcc=[bcc1,bcc2,bcc3,bcc4]
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

    def SendFinalApprovalEmail(self,title,name,remail,accno):
        try:
            Cursor=connection.cursor()  
            subject = "Trust Capital - Final Approval"
            email_from = 'cs@trusttc.com'
            bcc1="crm@trusttc.com"
            bcc2="backoffice@trusttc.com"
            bcc3="compliance@trusttc.com"
            bcc4="magt@trusttc.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno
                
            }  
            email_template_render=render_to_string("email/backoffice/TempAccountDetails.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

    def ClientAreaCredentialUpdateNotify(self,accno):
        try:
            Cursor=connection.cursor()  
            subject = "Client Area Credential Update"
            email_from = 'cs@trusttc.com'
            toEmail = "backoffice@trusttc.com"
            bcc1="crm@trusttc.com"
          
            bcc4="magt@trusttc.com"
            template_data={
             
                "account":accno
                
            }  
            email_template_render=render_to_string("email/backoffice/ClientAreaCredentialUpdateNotif.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[toEmail],bcc=[bcc1,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

    def ClientAreaCredentialUpdate(self,title,name,remail,accno):
        try:
            Cursor=connection.cursor()  
            subject = "Client Portal Update"
            email_from = 'cs@trusttc.com'
           
            bcc1="crm@trusttc.com"
          
            bcc4="backoffice@trusttc.com"
            template_data={
                "title":title,
                "name":name,
            }  
            email_template_render=render_to_string("email/backoffice/ClientAreaCredentialUpdate.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
    #Reset password 
    def sendResetPWD(self,title,name,remail,phonepwd):
        try:
            Cursor=connection.cursor()  
            subject = "Phone Password Reset"
            email_from = 'cs@trusttc.com'
           
            bcc1="crm@trusttc.com"
          
           
            template_data={
              
                "name":name,
                "password":phonepwd
            }  
            email_template_render=render_to_string("email/backoffice/ResetPPWDEmail.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
        #Reset password 
    def sendBankDetails(self,iban,bankname,reference,recbank,recbnkaddress,recreference):
        try:
            Cursor=connection.cursor()  
            subject = "Phone Password Reset"
            email_from = 'cs@trusttc.com'
           
            bcc1="crm@trusttc.com"
          
           
            # template_data={
              
            #     "name":name,
            #     "password":phonepwd
            # }  
            # email_template_render=render_to_string("email/backoffice/ResetPPWDEmail.html",template_data)
            # msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1])
            # msg.attach_alternative(email_template_render, "text/html")
            #msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 



       