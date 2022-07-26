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
            email_from = 'cs@trustcapital.com'
            bcc_mail="crm@trustcapital.com"
            cc_mail="magt@trustcapital.com"
            receiver_mail="backoffice@trustcapital.com"
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

    def newacc_password_notification(self,login):
        try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
            print("Email service---------------------------------------",login)   
            
        
            subject="NewAccount Passwords Notification"   
            email_from = 'cs@trustcapital.com'
            bcc_mail="crm@trustcapital.com"
            cc_mail="magt@trustcapital.com"
            receiver_mail="backoffice@trustcapital.com"
            template_data={
                "Login":login
            }
            print("Templatedata=====",template_data)
            email_template_render=render_to_string("email/NewAccountPasswordsNotification.html",template_data)
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
            email_from = 'cs@trustcapital.com'
            bcc_mail="crm@trustcapital.com"
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
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "salesrep":salesrep
            }  

            if (reason == 23):
                path = "email/backoffice/RejectionofAccountBelgium.html"
            if (reason == 25):
                path = "email/backoffice/RejectionofAccountThirdCountry.html"
            
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
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
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

    #send email template
    def sendtemplate(self,title,name,remail,tempId,repname):
        try:
            Cursor=connection.cursor()  
            print("email data====",title,name,remail,tempId)
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            # bcc2="backoffice@trustcapital.com"
            # bcc3="compliance@trustcapital.com"
            # bcc4="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "repname":repname
            }  
            print("Temp data=====",template_data)
            if (tempId == "6"):
                Subject = "Webinar Registration"
                path = "email/backoffice/WebinarRegistration.html"
            if (tempId == "8"):
                Subject = "KYC Documents"
                path = "email/backoffice/KYCNotification.html"
            if (tempId == "9"):
                Subject = "Account reached Stop Out "
                path = "email/backoffice/StopOut.html"
            if (tempId == "10"):
                Subject = "Margin Call Notification "
                path = "email/backoffice/MarginCall.html"
            if (tempId == "11"):
                Subject = "About Trust Capital"
                path = "email/backoffice/AboutTrustCapitalTC.html"
            if (tempId == "12"):
                Subject = "Unreachable"
                path = "email/backoffice/unreachable.html"
            if (tempId == "13"):
                Subject = "MetaTrader 4 Advantages"
                path = "email/backoffice/MetaTrader4Advantages.html"
            if (tempId == "14"):
                Subject = "Mobile Trading"
                path = "email/backoffice/MobileTrading.html"
            if (tempId == "15"):
                Subject = "Types Of Account"
                path = "email/backoffice/TypesOfAccounts.html"
            if (tempId == "16"):
                Subject = "Trading Instruments"
                path = "email/backoffice/TradingInstruments.html"
            if (tempId == "17"):
                Subject = "Spreads"
                path = "email/backoffice/Spreads.html"
            if (tempId == "18"):
                Subject = "Trust Capital - Missing POR"
                path = "email/backoffice/MissingProofofResidence.html"
            if (tempId == "19"):
                Subject = "Trust Capital - Missing ID"
                path = "email/backoffice/MissingId.html"
            print("Email",path,template_data)    
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=Subject,from_email=email_from,to=[remail],bcc=[bcc1])
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
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
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
      #Send Temperory Account Details
    def SendLiveAccountDetails(self,title,name,remail,accno,acctype):
        try:
            Cursor=connection.cursor()  
            subject = "Your Live Trust Capital Account Details"
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "acctype":acctype,
                "account":accno
                
            }  
            email_template_render=render_to_string("email/backoffice/LiveAccountDetails.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

    def SendNewAccountPasswords(self,title,name,remail,accno,mpassword, ppassword, ipassword):
        try:
            Cursor=connection.cursor()  
            subject = "New Account Passwords"
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "MPassword":mpassword,
                "account":accno,
                "PPassword":ppassword,
                "IPassword":ipassword
                
            }  
            email_template_render=render_to_string("email/backoffice/NewAccountPasswords.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1])
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
           
            
            email_from = 'cs@trustcapital.com'
            print("Mail======",title,name,remail,cardno,subject,cardtype)
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
            
            template_data={
                "title":title,
                "name":name,
                "cardno":cardno
                
            }  
            if cardtype=="Credit":
                if (status=="Approved"):
                    subject = "Credit Card Approved"
                    path="email/backoffice/CreditCardApproved.html"
                if(status=="Rejected"):
                    subject = "Credit Card Rejected"
                    path="email/backoffice/CreditCardRejected.html"
            if cardtype=="Debit":
                if (status=="Approved"):
                    subject = "Debit Card Approved"
                    path="email/backoffice/DebitCardApproved.html"
                if(status=="Rejected"):
                    subject = "Debit Card Rejected"
                    path="email/backoffice/DebitCardRejected.html"
            if cardtype=="Crypto":
                if (status=="Approved"):
                    subject = "Crypto Card Approved"
                    path="email/backoffice/CryptoCardApproved.html"
                if(status=="Rejected"):
                    subject = "Crypto Card Rejected"
                    path="email/backoffice/CryptoCardRejected.html"

            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
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
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno
                
            }  
            email_template_render=render_to_string("email/backoffice/FinalApprovalClient.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

    # def SendTempApprovalEmail(self,title,name,remail,accno,acctype):
    #     try:
    #         Cursor=connection.cursor()  
    #         subject = "Your Live Trust Capital Account Details"
    #         email_from = 'cs@trustcapital.com'
    #         bcc1="crm@trustcapital.com"
    #         bcc2="backoffice@trustcapital.com"
    #         bcc3="compliance@trustcapital.com"
    #         bcc4="magt@trustcapital.com"
    #         template_data={
    #             "title":title,
    #             "name":name,
    #             "account":accno,
    #             "acctype":acctype
    #         }  
    #         email_template_render=render_to_string("email/backoffice/TempAccountDetails.html",template_data)
    #         msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
    #         msg.attach_alternative(email_template_render, "text/html")
    #         msg.send(fail_silently=False)
    #         print("Email send-----------------------------------------------------------")  
                    

    #     except Exception as e:
    #         print("EXCEPTION-----------------------")  
    #     finally:
    #         Cursor.close() 

    def ClientAreaCredentialUpdateNotify(self,accno):
        try:
            Cursor=connection.cursor()  
            subject = "Client Area Credential Update"
            email_from = 'cs@trustcapital.com'
            toEmail = "backoffice@trustcapital.com"
            bcc1="crm@trustcapital.com"
          
            bcc4="magt@trustcapital.com"
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
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
          
            bcc4="backoffice@trustcapital.com"
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
            email_from = 'cs@trustcapital.com'
            
            
            bcc1="crm@trustcapital.com"
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
    def sendBankDetailsdraft(self,iban,bankname,reference,recbank,recbnkaddress,recreference):
        try:
            Cursor=connection.cursor()  
            subject = "Phone Password Reset"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
          
           
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
    #Send Bank Details
    def sendBankDetails(self,title,name,remail):
        try:
            # Cursor=connection.cursor()  
            subject = "Bank Transfer Details"
            email_from = 'cs@trustcapital.com'
            remail="oshin@trustlns.ae"
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            
           
            template_data={
                "title":title,
                "name":name                
            }  
            email_template_render=render_to_string("email/backoffice/BankTransferDetails.html",template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.attach_file("templates/email/backoffice/bankdetails.pdf")
            #mail=EmailMessage("BankDetails","",'cs@trustcapital.com',[remail],attachments="templates/email/backoffice/bankdetails.pdf")
            #mail.attach_file("templates/email/backoffice/bankdetails.pdf")
            msg.send(fail_silently=False)
            #mail.send()
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------",e)  
    
    
        #send alert message
    def sendBDocExpiry(self,title,name,remail,message):
        try:
            Cursor=connection.cursor()  
            subject = "Phone Password Reset"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            if(message=="15 Days Before POR Expiry Alert"):
                subject="POR Expiry Notification"
                path="email/backoffice/BeforePORExpiration.html"
            if(message=="15 Days Before POI Expiry Alert"):
                subject="POI Expiry Notification"
                path="email/backoffice/BeforePOIExpiration.html"
            if(message=="After POR Expiry Alert"):
                subject="POR Expiry Notification"
                path="email/backoffice/AfterPORExpiration.html"
            if(message=="After POI Expiry Alert"):
                subject="POI Expiry Notification"
                path="email/backoffice/AfterPOIExpiration.html"
           
            template_data={
                "title":name,
                "name":name,
                
            }  
            print("Subject=====",subject,path,title,name,remail)
            email_template_render=render_to_string(path,template_data)
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
    #Reject Live account documents
    def rejectLiveaccountDocs(self,title,name,remail,reasons):
        try:
            Cursor=connection.cursor()  
            print("Reason=======",reasons)
            subject = "Live Account Documents Rejected"
            if(reasons=="gen"):
                
                path="email/backoffice/RejectionGN.html"
            if(reasons=="por"):
                
                path="email/backoffice/RejectionPOR.html"
            if(reasons=="blurry"):
                path="email/backoffice/BlurryPassportReject.html"
            if(reasons=="expired"):
                path="email/backoffice/ExpiredPassportReject.html"

            email_from = 'cs@trustcapital.com'
            
            bcc1="crm@trustcapital.com"
            
            # # bcc2="magt@trustcapital.com"
            # # bcc3="backoffice@trustcapital.com"
          
           
            template_data={
                "title":title,
                "name":name,
            }  
            
            email_template_render=render_to_string(path,template_data)
            
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------",e)  
        finally:
            Cursor.close() 
    #send credit In confirmation
    def SendCreditInConfirmation(self,title,name,remail,accno,currency,amount):
        try:
            Cursor=connection.cursor()  
            subject = "Credit In Confirmation from Trust Capital"
            email_from = 'cs@trustcapital.com'
          
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno,
                "amount":amount
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/CreditinConfirmationfromTrustCapital_EN_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/CreditinConfirmationfromTrustCapital_EN.html",template_data)

            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
    #send credit out confirmation
    def SendCreditOutConfirmation(self,title,name,remail,accno,currency,amount):
        try:
            Cursor=connection.cursor()  
            subject = "Credit Out Confirmation from Trust Capital"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno,
                "amount":amount
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/CreditinConfirmationfromTrustCapital_EN_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/CreditinConfirmationfromTrustCapital_EN.html",template_data)

            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
     #send credit out confirmation
    def SendDepositConfirmationWallet(self,title,name,remail,accno,currency,amount):
        try:
            Cursor=connection.cursor()  
            subject = "Deposit Confirmation from Trust Capital"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno,
                "amount":amount
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/DepositConfirmationEWallet_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/DepositConfirmationEWallet_USD.html",template_data)

            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
    #deposit confirmation
    def SendDepositConfirmation(self,title,name,remail,accno,currency,amount):
        try:
            Cursor=connection.cursor()  
            subject = "Deposit Confirmation from Trust Capital"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno,
                "amount":amount
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/DepositConfirmationfromTrustCapital_EN_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/DepositConfirmationfromTrustCapital_EN.html",template_data)

            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 

     #withdrawal confirmation
    def SendWithdrawalConfirmation(self,title,name,remail,accno,currency,amount):
        try:
            Cursor=connection.cursor()  
            subject = "Withdrawal Confirmation from Trust Capital"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "account":accno,
                "amount":amount
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/WithdrawalConfirmationfromTrustCapital_EN_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/WithdrawalConfirmationfromTrustCapital_EN.html",template_data)

            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
     #Inter account transfer
    def SendInteraccountTransferConfirmation(self,title,name,remail,accdest,accsrc,currency,amount):
        try:
            Cursor=connection.cursor()  
            subject = "Inter Account Transfer Confirmation from Trust Capital"
            email_from = 'cs@trustcapital.com'
           
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "amount":amount,
                "accountdest":accdest,
                "accountsrc":accsrc
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/InterAccountTrfrConfromTrustCapital_EN_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/WithdrawalConfirmationfromTrustCapital_EN.html",template_data)

            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
     #Send Dormant Account Details
    def SendDormant(self,title,name,remail,accno,currency):
        try:
            Cursor=connection.cursor()  
            subject = "Dormant Account has deposited Money"
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                
                "account":accno
                
            }  
            if(currency=="EUR"):                
                email_template_render=render_to_string("email/backoffice/transaction/DormantCreditIn_EUR.html",template_data)
            else:
                email_template_render=render_to_string("email/backoffice/transaction/DormantCreditIn.html",template_data)
            
            msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 
            
    #Send Complaince
    def SendComplaince(self,title,name,remail,accno,currency,amount,income,flag):
        try:
            Cursor=connection.cursor()  
            
            email_from = 'cs@trustcapital.com'
            bcc1="crm@trustcapital.com"
            bcc2="backoffice@trustcapital.com"
            bcc3="compliance@trustcapital.com"
            bcc4="magt@trustcapital.com"
            template_data={
                "title":title,
                "name":name,
                "amount":amount,
                "account":accno
                
            }  
            if flag==4:

                if(currency=="EUR"):     
                    Subject = "A dormant account has deposited money"           
                    email_template_render=render_to_string("email/backoffice/transaction/DormantDeposit_EUR.html",template_data)
                else:
                    email_template_render=render_to_string("email/backoffice/transaction/DormantDeposit.html",template_data)
            if flag==5:
                if(currency=="EUR"):     
                    Subject = "Fund withdrawal before 3 trades"           
                    email_template_render=render_to_string("email/backoffice/transaction/Fundwithdrawalbefore3trades_EUR.html",template_data)
                else:     
                    Subject = "Fund withdrawal before 3 trades"           
                    email_template_render=render_to_string("email/backoffice/transaction/Fundwithdrawalbefore3trades_EUR.html",template_data)
            if flag==6:
                if(currency=="EUR"):     
                    Subject = "A dormant account has credited in"           
                    email_template_render=render_to_string("email/backoffice/transaction/DormantCreditIn_EUR.html",template_data)
                else:     
                    Subject = "A dormant account has credited in"           
                    email_template_render=render_to_string("email/backoffice/transaction/DormantCreditIn.html",template_data)
            if flag==7:
                if(currency=="EUR"):     
                    Subject = "Deposit exceeds 100K"           
                    email_template_render=render_to_string("email/backoffice/transaction/Depositexceeds100K_EUR.html",template_data)
                else:     
                    Subject = "Deposit exceeds 100K"           
                    email_template_render=render_to_string("email/backoffice/transaction/Depositexceeds100K.html",template_data)

            
            msg = EmailMultiAlternatives(subject=Subject,from_email=email_from,to=[remail],bcc=[bcc1,bcc2,bcc3,bcc4])
            msg.attach_alternative(email_template_render, "text/html")
            msg.send(fail_silently=False)
            print("Email send-----------------------------------------------------------")  
                    

        except Exception as e:
            print("EXCEPTION-----------------------")  
        finally:
            Cursor.close() 




       