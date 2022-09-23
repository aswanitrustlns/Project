from audioop import reverse
from cmath import log
from email.message import Message
from operator import add

from time import strptime
from django.db import connection
from datetime import datetime, timedelta
from ctypes import *
import subprocess
import win32com.client
import random
import string
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
import imaplib
import email
import html2text
from .emailservices import EmailServices

emailservice=EmailServices()

class Selector:    
    
    #Get logged in user info
    def get_loged_user_info(self,username):
       
        try:
            Cursor=connection.cursor()            
            Cursor.execute("set nocount on;exec SP_GetLoginDetails %s",[username])
            UserId=Cursor.fetchone()
            UserId=UserId[0]          

        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return UserId

    #DLL connection in server
    def dll_connection(self,username,server_name,password):
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        ConnectToServer_Login = hllDll.ConnectToServer_Login
        hllDll.ConnectToServer_Login.argtype = c_char_p,c_int,c_char_p
        hllDll.ConnectToServer_Login.restype = c_int
        username=int(username)
        login = c_int(username)
        connect=ConnectToServer_Login(c_char_p(server_name.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value)
        return connect
    

    #Exe connectivity in local
    def exe_connection(self,username,server_name,password):        
        connect=subprocess.call(["C:\\Aswani\\pythonmanager\\manager_python.exe","1",server_name,username,password])
        return connect


    # Method to find the logged in user role(admin,salesrep etc)

    def user_role_selection(self,userId):
        
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetPermissions %s",[userId])
            user_role=Cursor.fetchone()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return user_role

    # User name from table
    def get_user_name(self,userId):
        try:  
            Cursor=connection.cursor()
            Cursor.execute("SELECT UserName,Email FROM tbl_User where UserID=%s",[userId])
            
            UserData=Cursor.fetchone()
           
            UserName=UserData[0] 
            print("User name======================",UserName)
            mailInfo=UserData[1]  
            print("Email==========================",mailInfo)         
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return UserName,mailInfo
    
    # Get Notification
    def get_notification_data(self,userId):
        try:
            Cursor=connection.cursor()
            Cursor.execute("exec SP_GetSummaryToday  %s",[userId])
            notifications = Cursor.fetchall()     
            print("Notification============================",notifications)       
            while (Cursor.nextset()):
                notification_count = Cursor.fetchall()                
                notify_count=notification_count[0]
                notification_count=notify_count[0]
                print("**************************",notification_count)
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return notification_count,notifications

    #Get phone number country code

    def get_country_code(self,phone_num):
        try:
            Cursor=connection.cursor()
            Cursor.execute("SELECT ID FROM tbl_Country where CCode=%s",[phone_num])
            country_code=Cursor.fetchone()
            
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return country_code
    #Get All Country
    def get_all_country(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("SELECT ID,Country FROM tbl_Country")
            country_list=Cursor.fetchall()
            
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return country_list
    #Get Country Code
    def get_code_country(self,cry_id):
        try:
            
            Cursor=connection.cursor()
            Cursor.execute("SELECT Code FROM tbl_Country where ID=%s",[cry_id])
            country_list=Cursor.fetchall()
            if country_list:
                country_list=country_list[0]
                country_list=country_list[0]
            print("Country code===",country_list)
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return country_list

    #Merge ticket procedure call
    def merge_ticket(self,ticket,email1,email2,mobile,telephone):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_MergeTicket %s,%s,%s,%s,%s",[ticket,email1,email2,mobile,telephone])
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
    
    #User Permission check in lead registation
    def user_permission_check(self,UserId,ticket,login):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_CheckUserPermission_PY %s,%s,%s",[UserId,ticket,login])
            user_permission=Cursor.fetchone() 
                
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return user_permission
    
    #Get leads
    def get_leads(self,lead,from_date,to_date):
        try:
            Cursor=connection.cursor()
            date_today=datetime.today().date()  

            date_today=date_today.strftime("%Y-%m-%d")
           
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
            else:
                date_yesterday = datetime.today()-timedelta(1)
                
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")  
            Cursor.execute("set nocount on;exec SP_LeadsCount_PY")
            leads_count = Cursor.fetchone()
            if lead=="all":
                print("Load all data----")
                Cursor.execute("SET NOCOUNT ON;exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",[from_date,to_date,'',0,0,'',1])
                print("statement executed-----------------------------------------------")
                leads_data=Cursor.fetchall() 
            else:
                Cursor.execute("SET NOCOUNT ON;exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",[date_yesterday,date_today,'',0,0,'',1])
                leads_data=Cursor.fetchall()
                
               
            for index, item in enumerate(leads_data):
                itemlist = list(item)
                dt=itemlist[0]
                
                itemlist[0]=datetime.strptime(dt, '%Y-%m-%d').date()
                
               

                leads_data[index] = tuple(itemlist)
          
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return leads_data,leads_count
    #Get Lead Page click
    def get_leads_clicks(self,status):
        try:
            leads_data=[]
            Cursor=connection.cursor()
            print("====================================",status)
            # Cursor.execute("set nocount on;exec SP_LeadsCount_PY")
            # leads_count = Cursor.fetchone()
            # print("Leads count==========================",leads_count)
            # if(leads_count):
            Cursor.execute("set nocount on;exec SP_LeadsListing_PY %s",[status])
            leads_data=Cursor.fetchall()
            print("Leads data",len(leads_data))
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return leads_data
    
    #Get Tickets
    def get_tickets(self,userId,ticket):
        try:
            Cursor=connection.cursor()
           
            print("------------------------------",ticket)
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                    date_yesterday = datetime.today()-timedelta(3)
            else:
                date_yesterday = datetime.today()-timedelta(1)
                    
            date_yesterday=date_yesterday.strftime("%Y-%m-%d") 
            if(ticket == "pending"):
                
                print("Laod Pending")
                Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,date_yesterday,date_today,'P',0])
                _tickets=Cursor.fetchall()

            if(ticket=="resolved"):
                print("Load resolved")            
                Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,date_yesterday,date_today,'R',0])
                _tickets=Cursor.fetchall()
            if(ticket=="dormant"):
                
                print("dormant tickets")
                Cursor.execute("exec SP_GetDormantSalesLeadsPaginate_PY %s,%s,%s",[userId,"P",userId])
                _tickets=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return _tickets  
    #Get all tickets

    def get_all_tickets(self,userId,ticket,from_date,to_date):
        try:
            Cursor=connection.cursor()
            if(ticket == "pending"):                    
                print("Load all pending")
                Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,from_date,to_date,'P',0])
                _tickets=Cursor.fetchall()
            if(ticket=="resolved"):
               
                print("Load all resolved")
                Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,from_date,to_date,'R',0])
                _tickets=Cursor.fetchall()
            
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close() 
        return _tickets

    #Get new accounts count
    def get_new_accounts_count(self,from_date,to_date):
        try:
            
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[from_date,to_date])
           accounts_count=Cursor.fetchone()
           print("Accounts count",accounts_count)
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        
        return accounts_count
     #Get new accounts count for variants
    def get_new_accounts_count_variants(self,from_date,to_date,change):
        try:
            
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetNewAccountsListing  %s,%s,%s",[from_date,to_date,change])
           accounts_count=Cursor.fetchone()
           print("Accounts count",accounts_count)
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        
        return accounts_count
    
    # Get New Accounts page data
    def get_new_accounts(self,change,status,from_date,to_date):
        try:
           Cursor=connection.cursor()
           date_today=datetime.today().date()    
           date_today=date_today.strftime("%Y-%m-%d")
           week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
           if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
           else:
                date_yesterday = datetime.today()-timedelta(1)
           date_yesterday=date_yesterday.strftime("%Y-%m-%d")
           print("Load all ---",change)
           if(change == "All"):
                print("All status----------------",status)
                Cursor.execute("set nocount on;exec SP_GetNewAccountsList %s,%s,%s",[from_date,to_date,status])  
                live_accounts=Cursor.fetchall()
           else: 
                print("Else executed-=====",date_yesterday,date_today)
                Cursor.execute("set nocount on;exec SP_GetNewAccountsList %s,%s,%s",[date_yesterday,date_today,change])  
                live_accounts=Cursor.fetchall()
           print("Length of dat======================",live_accounts)  
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return live_accounts

     # Get New Accounts click data
    def get_new_accounts_click(self,status,from_date,to_date):
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetNewAccountsListing %s,%s,%s",[from_date,to_date,status])  
           live_accounts=Cursor.fetchall()
          
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return live_accounts    
   # Get New Accounts page data
    def get_new_accounts_filter(self,change):
        try:
           Cursor=connection.cursor()
           date_today=datetime.today().date()    
           date_today=date_today.strftime("%Y-%m-%d")
           week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
           if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
           else:
                date_yesterday = datetime.today()-timedelta(1)

           date_yesterday=date_yesterday.strftime("%Y-%m-%d")
           
           print("Else executed-=====",date_yesterday,date_today)
           Cursor.execute("set nocount on;exec SP_GetNewActsFromDashboard %s,%s,%s",[date_yesterday,date_today,change])  
           live_accounts=Cursor.fetchall()
           print("Length of dat======================",live_accounts)  
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        # for index, item in enumerate(live_accounts):
        #         itemlist = list(item)
        #         dt=itemlist[0]
                
        #         itemlist[0]=datetime.strptime(dt, '%Y-%m-%d').date()
                
               

        #         live_accounts[index] = tuple(itemlist)
        return live_accounts
        
#Duplicate lead check
    def check_duplicate(self,phone,email):
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec TC_GetDuplicatePhoneList %s,%s",[phone,email])
           duplicate=Cursor.fetchone()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return duplicate
#close lead 
    def close_lead(self,demoid,ticket):
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_CloseLead %s,%s",[demoid,ticket])
           
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        
#create new ticket
    def create_new_ticket(self,demoid):
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetLeadDetailsByID %s",[demoid])
           ticket_data=Cursor.fetchone()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return ticket_data

#Get Leads Count
    def get_leads_count(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_LeadsCount_PY")
            leads_count=Cursor.fetchone()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return leads_count
    
# Logout Procedure call

    def user_logout(self,userId):
        try:
           Cursor=connection.cursor()
           
           Cursor.execute("set nocount on;exec SP_SetUserStatus %s",[userId])           
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()

#Email template rendering and send Mail

    def mailSend(self,token,subject,bcc,cc,template,sendername):
        try:
            print("token--------------",token)
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLastMeetingDetails %s",[token])
            meeting_details=Cursor.fetchone()
            Cursor.execute("set nocount on;exec SP_GetTicket_PY %s",[token])
            client_details=Cursor.fetchone()
            print("Meeting details--------------------------",meeting_details)
            print("Client details----------------",client_details)
            
            email_from = 'cs@trusttc.com'
            receiver=client_details[2]
          
            print("Receiver===========================",receiver)

            template_data={
                "title":client_details[0],
                "name":client_details[1],
                "sender":sendername,
                "date":meeting_details[0],
                "time":meeting_details[1],
                "location":meeting_details[2],
                "purpose":meeting_details[3]
            }
            email_template_render=render_to_string("email/"+template,template_data)
            #email_template_render=get_template("email/MeetingReminder.html",template_data)
            try:
                #send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
                # msg=EmailMessage(subject,email_template_render,email_from,[receiver],[receiver])
               
                msg = EmailMultiAlternatives(subject=subject,from_email=email_from,to=[receiver], bcc=[bcc], cc=[cc])
                msg.attach_alternative(email_template_render, "text/html")
                msg.send(fail_silently=False)
                
            except BadHeaderError:
                print("EXCEPTION-----------------------")       
        except Exception as e:
            print("Exception--------------------------",e)
        finally:
            Cursor.close()
#cancel Meeting
    def cancel_meeting_mail(self,userId,token):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLastMeetingDetails %s",[token])
            meeting_details=Cursor.fetchone()
            Cursor.execute("set nocount on;exec SP_InsertMeeting  %s,%s,%s,%s,%s,%s,%s,%s,%s",[meeting_details[0],meeting_details[1],meeting_details[2],meeting_details[3],meeting_details[4],2,userId,token,meeting_details[6]])
            Cursor.execute("set nocount on;exec SP_GetTicket_PY %s",[token])
            client_details=Cursor.fetchone()
            print("Meeting details--------------------------",meeting_details)
            print("Client details----------------",client_details[2])
            subject="Trust Capital - Meeting Cancelled"
            email_from = settings.EMAIL_HOST_USER
            receiver=client_details[2]
            #receiver='aswani.technology@gmail.com'
            template_data={
                "title":client_details[0],
                "name":client_details[1],
                "sender":client_details[3],
                
            }
            print("Meeting cancelled-------")
            email_template_render=render_to_string("email/MeetingCancelled.html",template_data)
            try:
                send_mail(subject," ",email_from,[receiver],fail_silently=False,html_message=email_template_render)
            except BadHeaderError:
                print("EXCEPTION-----------------------")       
        except Exception as e:
            print("Exception--------------------------",e)
        finally:
            Cursor.close()
    #Set Assesement Score
    def get_meeting_score(self,ticket):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetMeetingScore %s",[ticket])
            meeting_score=Cursor.fetchone()
            print("Meeting Score-----------------------------",meeting_score)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return meeting_score
    
    #Set live chat logs

    def get_livechat_logs(self,ticket):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLiveChatLogs %s",[ticket])
            chat_log=Cursor.fetchall()
            
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return chat_log

    # # Get leads details by ticket and userid
    # def get_leads_details(self,ticket,mailId):
    #     try:
    #         Cursor=connection.cursor()
    #         Cursor.execute("set nocount on;exec SP_GetLeadDetailsByTicket %s,%s",[ticket,mailId])
    #         leads_details=Cursor.fetchone()
    #         print("Leads details-----------------------------",leads_details)
        # except Exception as e:
        #     print("Exception------",e)
        # finally:
        #     Cursor.close()
    #     return leads_details

    #dll open demo function call
    


    #Open demo account
    def open_demo_account(self,title,name,email,phone,country):
        #call dll function
        try:
            Cursor=connection.cursor()
            Cursor.execute("SELECT cOUNTRY FROM tbl_Country where ID=%s",[country])
            country_name=Cursor.fetchone()
        
            password=random_ped_gen()
            demo_account=dll_demo_account(name,email,phone,country_name,password)
            if(demo_account != 0):
                emailservice.demo_account_email(title,name,demo_account,password,email)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()

    



    def resolve_ticket(self,ticket,userid,reason):
        livestatus=""
        msg="Ticket Resolved"
        try:
           Cursor=connection.cursor()
           print("Ticket========================",ticket)
           Cursor.execute("set nocount on;exec SP_GetAccountStatusByTicket %s",[ticket])
           ticket_status=Cursor.fetchone()
           print("Ticket status=========================",ticket_status)
           if(ticket_status):
                ticket_status=ticket_status[0]
                if(ticket_status=="Live"):
                        msg="Cannot resolve ticket with Account No"
           else:
                        Cursor.execute("set nocount on;exec SP_ResolveTicket %s,%s,%s",[ticket,userid,reason])
                        value=Cursor.fetchone()
                        print("Resolve value=====",value)
                        if value:
                            value=value[0]
                            if(value==0):
                                msg="'Ticket Resolved Successfully"
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        print("Ticket Resolve message======",msg)
        return msg
    
    def get_mail_inbox(self):
        inbox_list=[]
        i=1
        try:
            # outlook = win32com.client.Dispatch("Outlook.Application")
            # mapi=outlook.GetNamespace("MAPI")
            # inbox = mapi.GetDefaultFolder(6) # 5 for send items----

            # messages = inbox.Items
            # messages.Sort("[ReceivedTime]", True)
            # inbox_count=len(messages)
            # for message in messages:
            #     subject = message.Subject
            #     sender = message.SenderEmailAddress
            #     received_tym=message.ReceivedTime
            #     inbox_data=(subject,sender,received_tym)
            #     inbox_list.append(inbox_data)
            mail = imaplib.IMAP4_SSL(host=settings.EMAIL_HOST)

            mail.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
            status, messages=mail.select("INBOX")
            _, selected_mails = mail.search(None,'(ALL)')
            inbox_count=len(selected_mails[0].split())
            print("length===========",len(selected_mails[0].split()))
            for i in range(1, inbox_count):
                res,msg = mail.fetch(str(i), '(RFC822)')
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        
                        subject=msg["subject"]
                        sender=msg["from"]
                        received_tym=msg["date"]
                        if received_tym:
                            received_tym=received_tym[0:16]
                        else:
                            received_tym=""
                        
                        # received_tym=datetime.strptime(received_tym,'%d%m%y')
                        # print("Received date===========",type(received_tym))
                        
                        inbox_data=(subject,sender,received_tym,msg["Message-ID"])
                        print("Inbox daattttt",i+1)
                        inbox_list.append(inbox_data)

            print("Length of inbox=====",len(inbox_list))
           
        except Exception as e:
            print("Exception------",e)
        finally:
            pass
        inbox_list.reverse()
     
        return inbox_count,inbox_list
#Email template send items----
    def template_send_items_list(self,emailname):
        count=0
        try:
            inbox_list=[]
            username="crm@trusttc.com"
            app_password="Vydw&663"

            mail_server = 'mail.trusttc.com'

            mailbox = imaplib.IMAP4_SSL(mail_server)

            mailbox.login(username, app_password)
            mailbox.select("INBOX")
            search_cr='(TO "'+emailname+'")'
            print("Search mail=============================",search_cr)
            type, selected_mails = mailbox.search(None,search_cr) #mail.search based criteria mail.search(None,'(FROM "email" SUBJECT "the subject" UNSEEN)')
            count=len(selected_mails[0].split())
            print("Total Messages " , len(selected_mails[0].split()))

            # for i in range(1, int(messages[0])):
            for i in selected_mails[0].split():
                res, msg = mailbox.fetch(i, '(RFC822)')   
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject=msg["subject"]
                        receive_tym=msg["date"]
               
                        # print("message=========================",msg["Message-ID"])

                        if receive_tym:
                                receive_tym=receive_tym[0:11]
                        inbox_data=(subject,receive_tym,msg["Message-ID"])
                        
                        inbox_list.append(inbox_data)
        except Exception as e:
            print("Exception------",e)
        finally:
            pass
        inbox_list.reverse()
        return count,inbox_list
# Send Items for manage tickets
    def read_mail_senditems(self,emailname,message):
        print("read senditems",message)
        username="crm@trusttc.com"
        app_password="Vydw&663"

        mail_server = 'mail.trusttc.com'

       
        mail = imaplib.IMAP4_SSL(mail_server)
        message_data=""
        subject=""
        sender=""
        mail.login(username, app_password)
        status, messages=mail.select("INBOX")
        search_cr='(TO "'+emailname+'")'
        print("Searched Id=====",search_cr)
        elem, selected_mails = mail.search(None,search_cr)
        
       
        for i in selected_mails[0].split():
            res, msg = mail.fetch(i, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    print("+++++++++++++++++++++++++msg id",msg["Message-ID"])
                    if(message == msg["Message-ID"]):
                        print("Message")
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        print("Equal================== and content type",content_type)
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":
                                    print("Content type------",part.get_content_type())
                                    message = part.get_payload(decode=True)
                                    message_data=message.decode()                                                                  
                                    break
                                if part.get_content_type()=="text/html":
                                    text = f"{part.get_payload(decode=True)}"
                                    html = text.replace("b'", "")
                                    h = html2text.HTML2Text()
                                    h.body_width = 0
                                    h.ignore_links = False                                 
                                    output = (h.handle(f'''{html}''').replace("\\t", " "))
                                    output = output.replace("\\n", " ")
                                    output = output.replace("\\r", " ")
                                    output = output.replace("'", "")
                                    output = output.replace("\\", "")
                                    output = output.replace("---", "")
                                    output = output.replace("|", "")
                                    print("Outpu----------------",output)
                                    message_data=output
                                
                            
        
        return message_data,subject,sender

 # Read mail inbox
    def read_mail_inbox(self,message):
        print("read mail inboxxxx",message)
        mail = imaplib.IMAP4_SSL(host=settings.EMAIL_HOST)
        message_data=""
        subject=""
        sender=""
        mail.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        status, messages=mail.select("INBOX")
        _, selected_mails = mail.search(None,'(ALL)')
        inbox_count=len(selected_mails[0].split())
       
        for i in range(1, inbox_count):
            res, msg = mail.fetch(str(i), '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    if(message == msg["Message-ID"]):
                        print("Message")
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        print("Equal================== and content type",content_type)
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":
                                    print("Content type------",part.get_content_type())
                                    message = part.get_payload(decode=True)
                                    message_data=message.decode()                                                                  
                                    break
                                if part.get_content_type()=="text/html":
                                    text = f"{part.get_payload(decode=True)}"
                                    html = text.replace("b'", "")
                                    h = html2text.HTML2Text()
                                    h.body_width = 0
                                    h.ignore_links = False                                 
                                    output = (h.handle(f'''{html}''').replace("\\t", " "))
                                    output = output.replace("\\n", " ")
                                    output = output.replace("\\r", " ")
                                    output = output.replace("'", "")
                                    output = output.replace("\\", "")
                                    output = output.replace("---", "")
                                    output = output.replace("|", "")
                                    print("Outpu----------------",output)
                                    message_data=output
                                
                            
        
        return message_data,subject,sender,inbox_count
    

# #Get activities log    
#     def get_activity_log(self,ticket):

#         try:
            

#             now = datetime.now()
#             current_time = now.strftime("%H:%M:%S")
#             Cursor=connection.cursor()
#             ticket=ticket.strip()
#             print("Ticket----------------------------------activity",ticket,current_time)
#             Cursor.execute("set nocount on;exec SP_GetTicketLogs %s,%s",[ticket,current_time])
#             activity_log=Cursor.fetchall()
#             print("Activity log-----------------------------------",activity_log)
#         except Exception as e:
#             print("Exception------",e)
#         finally:
#             Cursor.close()
#         return activity_log

#Get all meetings
    def get_all_meeting(self,ticket):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetAllMeetings  %s",[ticket])
            all_meetings=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return all_meetings
#Get all meetings
    def get_last_meeting(self,ticket):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLastMeetingDetails %s",[ticket])
            all_meetings=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return all_meetings

# #send meeting confirmation mail

#     def send_meeting_mail(self):
#         pass

# #cancel meeting mail
#     def cancel_meeting_mail(self):
#         pass
#view Document
    def view_document(self,ticket):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetMeetingDocs %s",[ticket])
            all_documents=Cursor.fetchall()
            print("All documents-----",all_documents)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return all_documents
    
    # Get Lead Score
    def get_lead_score(self,ticket):
        try:
            lead_score=0
            Cursor=connection.cursor()
            ticket=ticket.strip()
            print("ticket====",ticket)
            Cursor.execute("set nocount on;exec SP_GetLeadScore %s",[ticket])
            lead_score=Cursor.fetchall()
            if lead_score:
                lead_score=lead_score[0]
                lead_score=lead_score[0]
           
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return lead_score
    
    # Get Ticket Summary
    def get_ticket_summary(self,ticket):
        summary_list=[]
        
        try:
            ticket=ticket.strip()
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSalesSummary %s",[ticket])
            ticket_summary=Cursor.fetchall()
           
            for summary in ticket_summary:
                
                summary_text=summary[1].split(":",1)  #index out of range
               
                summary_list.append({
                    'summary_head':summary_text[0],
                    'summary_text':summary_text[1]
                })
            print("Summary list===",summary_list)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return summary_list
    
    #Get sales summary
    def get_sales_summary(self,ticket):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetMeetingScore %s",[ticket])
            sales_summary=Cursor.fetchall()
     
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return sales_summary

    #Get Lead details
    def get_lead_details(self,ticket,userid):
        try:
            countryName=""
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLeadDetailsByTicket %s,%s",[ticket,userid])
            lead_details=Cursor.fetchone()
          
            # if (lead_details):
            #     country=lead_details[10]
            #     if(country):
            #         country=country[0]
            #         Cursor.execute("SELECT COUNTRY FROM tbl_Country where CCode=%s",[country])
            #         countryName=Cursor.fetchone()
            #         countryName=countryName[0]
            #     print("Country================================",countryName)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return lead_details

    #Get Activities log
    def get_activities_log(self,ticket):
        try:
            Cursor=connection.cursor()
            current=datetime.now()
            ticket=str(ticket)
            log_time=current.strftime("%H:%M:%S")
            print("Current timeeeeeeeeeeeeeeeeeee",log_time)
            Cursor.execute("set nocount on;exec SP_GetTicketLogs %s,%s",[ticket,log_time])
            activity_logs=Cursor.fetchall()
           
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return activity_logs

    #Name search
    def get_name_search(self,searched,userId):
        name_search_list=0
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_CheckForMultipleName %s",[searched])
            search_count=Cursor.fetchone()
            search_count=search_count[0]
            print("Search count--------------------------------",search_count)
            if(search_count>0):
                Cursor.execute("set nocount on;exec SP_SearchName %s,%s",[searched,userId])
                name_search_list=Cursor.fetchall()

        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return name_search_list
    #Get account number
    def get_account_no(self,ticket):
        accountno=""
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetMultipleAccountsTicket %s",[ticket])
            accountno=Cursor.fetchone()
            if accountno:
                accountno=accountno[0]
            
                print("Account number--------------------------------",accountno)
           

        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return accountno


    #Phone search
    def get_phone_search(self,searched,userId):
        try:
            phone_search_list=0
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_CheckForMultiplePhone %s",[searched])
            search_count=Cursor.fetchone()
            search_count=search_count[0]
            print("Search count--------------------------------",search_count)
            if(search_count > 0):
                Cursor.execute("set nocount on;exec SP_SearchPhone %s,%s",[searched,userId])
                phone_search_list=Cursor.fetchall()

        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return phone_search_list
    

    #Email search
    def get_mail_search(self,searched,userId):
        try:
            mail_search_list=0
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_CheckForMultipleEmail %s",[searched])
            search_count=Cursor.fetchone()
            search_count=search_count[0]
            print("Search count--------------------------------",search_count)
            if(search_count>0):
                Cursor.execute("set nocount on;exec SP_SearchEmail %s,%s",[searched,userId])
                mail_search_list=Cursor.fetchall()

        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return mail_search_list
    
    #Account no status check
    def account_status_check_update(self,accountno,ticket,request):
        msg=""
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetAccountStatus %s",[accountno])
            status=Cursor.fetchone()
            if status:
                status=status[0]
            print("Account update status========================",status)
            if(status=="Live" or status=="ReadOnly"):
                msg="You dont have permission to update live account details"
                print("You dont have permission to update live account details")
            else:
               update_result=update_account_client_datails(request)
               emailservice.account_update_email(accountno,ticket,request,update_result)
               msg="Updated Successfully"
               if(update_result!=None):
                    pass
               print("Update result with account number=====",update_result) 
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return msg

     #Ticket status check
    def ticket_validity_check_update(self,ticket,request):
        msg=""
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_IsTicketValid %s",[ticket])
            valid=Cursor.fetchone()
            print("valid check===========",valid)
            valid=valid[0]
            if(valid==1):             
               update_ticket(request)


        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return msg
    #Email template send---

    def email_template_selection(self,lang,subject,fromaddr,to,title,name,userId,ticket):
        try:
            Cursor=connection.cursor()
            emailservice.send_email_templates(lang,subject,to,title,name)
            print("Selector----",lang,subject,fromaddr,to,title,name)
            history="Send --xxxxxx[Eng]-- SMS for Ticket xxx"
            chattype=""
            dept=""
            Cursor.execute("set nocount on;exec SP_UpdateChatAndLog %s,%s,%s,%s,%s",[userId,history,chattype,ticket,dept])
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()

    def get_last_comment(self,ticket,UserId):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLastComment %s,%s",[ticket,UserId])
            comment=Cursor.fetchone()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return comment
        
    def save_reminder(self,userid,ticket,subject,date,time,login,color,mail):
        print("Selcetor saveeeee")
        print("----------------------",userid,ticket,subject,date,time,mail)
        try:
            subject=subject+ticket
            badge="Green"
            desc=subject
            rdate=date
            if login=="":
                login=0
            
            Cursor=connection.cursor()
            date_today=datetime.today().date()  

            date_today=date_today.strftime("%Y-%m-%d")
            Cursor.execute("set nocount on;exec SP_SetReminder %s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[userid,subject,desc,ticket,date_today,time,rdate,color,login,badge])
            fulltime=date+" "+time
            apdate=datetime.strptime(fulltime,'%Y-%m-%d %H:%M')
            
            print("Date==========================================",apdate)
            # Cursor.execute("SELECT email FROM tbl_User where UserID=%s",[userid])
            #email=Cursor.fetchone()
            # mail="aswani@trustlns.ae"
            outlook = win32com.client.Dispatch("Outlook.Application")
            apdate=apdate.strftime("%Y-%m-%d %H:%M")
            appt = outlook.CreateItem(1) # AppointmentItem
            appt.Start = apdate # yyyy-MM-dd hh:mm
            appt.Subject = "Meeting Test"
            appt.Duration = 60 # In minutes (60 Minutes)
            appt.Location = "Dubai"
            appt.ReminderSet = True
            appt.MeetingStatus = 1 # 1 - olMeeting; Changing the appointment to meeting. Only after changing the meeting status recipients can be added
            appt.Recipients.Add(mail) # Don't end ; as delimiter

            appt.Save()
            appt.Send()
            print("Outlook reminder send")
            Cursor.execute("set nocount on;exec SP_InsertTicketLogs %s,%s,%s,%s",[userid,subject,"Reminder",ticket])
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
    #SInsert ticket logs procedure
    def insert_ticket_logs(self,userid,logdata,logtype,ticket):
        try:
            Cursor=connection.cursor()
            print("Insert ticket logs data=======",userid,logdata,logtype,ticket)
            Cursor.execute("set nocount on;exec SP_InsertTicketLogs %s,%s,%s,%s",[userid,logdata,logtype,ticket])
            print("Ticket log inster done")
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()

    def get_sticky_text(self,ticket):
            try:
                sticky_data=""
                Cursor=connection.cursor()
                Cursor.execute("set nocount on;exec SP_GetStickyNotes %s",[ticket]) 
                sticky_data=Cursor.fetchone()
                if sticky_data:
                    sticky_data=sticky_data[0]
            except Exception as e:
                print("Exception------",e)
            finally:
                Cursor.close()
            return sticky_data
    def save_Sticky_text(self,note,userid):
        print("Sticky selector")
        try:
            Cursor=connection.cursor()
            login=0
            flag=0
            
            Cursor.execute("set nocount on;exec SP_StickyNotes %s,%s,%s,%s",[login,flag,note,userid]) 
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()



    #Send email from Managetickets
    def email_compose(self,to,sub,emailbody):
        try:
           
            emailservice.send_mail_manageTicket(to,sub,emailbody)
            print("Selector----",to,sub,emailbody)
            
        except Exception as e:
            print("Exception------",e)
        finally:
            pass
    #Get Upcoming seminar
    def get_upcoming_seminar(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_UpcomingSeminars") 
            seminarlist_upcoming=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return seminarlist_upcoming
    # Register Seminar
    def register_seminar(self,title,name,to_addr,seminartitle,ticket,userid):
        register_msg=""
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_SeminarConfirmation %s,%s,%s",[ticket,userid,seminartitle]) 
            register_msg=Cursor.fetchone()
            print("Register mesage================",register_msg)
            
            if register_msg:
                if(register_msg[0]=='Seminar Confirmed Successfully'):
                   emailservice.seminar_confirmation_email(title,name,to_addr,seminartitle)
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return register_msg
    #Get seminar list
    def get_seminar_list(self,ticket):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetSeminarDetailsforTicket %s",[ticket]) 
            seminarlist=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return seminarlist
    #Update seminar status
    def update_seminar_status(self,ticket,status,seminar,userid):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_UpdateAttending %s,%s,%s,%s",[ticket,status,seminar,userid]) 
            
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
    #Webinar attended
    def get_webinar_attended(self,ticket):
        webinars=[]
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetWebinarAttended  %s",[ticket]) 
            webinars=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return webinars
    
        



    

    


    
    # def sendReminder(self,datetime):
    #     outlook = win32com.client.Dispatch("Outlook.Application")
    #     appt = outlook.CreateItem(1) # AppointmentItem
    #     appt.Start = datetime # yyyy-MM-dd hh:mm
    #     appt.Subject = "Meeting Test"
    #     appt.Duration = 60 # In minutes (60 Minutes)
    #     appt.Location = "Dubai"
    #     appt.ReminderSet = True
    #     appt.MeetingStatus = 1 # 1 - olMeeting; Changing the appointment to meeting. Only after changing the meeting status recipients can be added
    #     appt.Recipients.Add("aswani@trustlns.ae") # Don't end ; as delimiter

    #     appt.Save()
    #     appt.Send()

        
        

#Random password generator
def random_ped_gen():
    all = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.sample(all,8))
    return password

#dll demo account
def dll_demo_account(name,email,phone,country,password):
        demoserver = "50.57.14.224:443"
        demopwd = "Tc2022"
        demouser = "601"    
        # name="Aswani test"
        # email="aswani@trustlns.ae"
        # phone='0565662073'
        # country='United Arab Emirates'
        # password="123asw89"
        details="NAME="+name+"^EMAIL="+email+"^PHONE="+phone+"^USER_COUNTRY"+country+"^USER_PASSWORD"+password
        received="reciveddata"
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        DemoAccount_Create = hllDll.DemoAccount_Create
        hllDll.DemoAccount_Create.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.DemoAccount_Create.restype = c_int
        username=int(demouser)
        login = c_int(username)
        connect=DemoAccount_Create(c_char_p(demoserver.encode('utf-8')).value,login.value,c_char_p(demopwd.encode('utf-8')).value,c_char_p(details.encode('utf-8')).value)
        return connect



def update_ticket(request):
         
     try:
        Cursor=connection.cursor()
       
        name=request.POST.get('firstname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        subject=request.POST.get('subject')
        ticket=request.POST.get('formticket')
        print("Countryyyy",ticket)
        country=int(request.POST.get('country'))
        print("Type of country",type)
        clientarea=request.POST.get('clientarea')
        potential=0
        city=request.POST.get('city')
        address=request.POST.get('address')
        if (address ==""):
            address=None
        state=request.POST.get('state')
        if(state==""):
            state=None
        zipcode=request.POST.get('zipcode')
        if (zipcode==""):
            zipcode=0
        # nationality=request.POST.get('nationality')
        nationality=0
        profession=request.POST.get('profession')
        dob=request.POST.get('dob')
        if(dob==""):
            dob=None
        income=request.POST.get('income')
        if income:
            income=int(income)
        else:
            income=None
        # networth=request.POST.get('networth')
        networth=0
        experience=int(request.POST.get('experience'))
        hear=request.POST.get('hearfrom')
        # email2=request.POST.get('email2')
        # phone2=request.POST.get('phone2')
        email2=None
        phone2=None
        # country2=request.POST.get('country2')
        country2=0
        # noemail=request.POST.get('noemail')
        noemail=0
        title=request.POST.get('title')
        # hyplinks=request.POST.get('hyplinks')
        hyplinks="NULL"
        appform=int(request.POST.get('appform'))
        age=request.POST.get('age')
      
        category=None
        userId=int(request.session.get('UserId'))
        language=int(request.POST.get('language'))
        training=request.POST.get('training')
        print("Staus ticket update------",name,email,phone,subject,ticket,country,clientarea,potential,city,address,state,zipcode,nationality,profession,dob,income,networth,experience,hear,email2,phone2,country2,noemail,title,hyplinks,appform,age,category,userId,language,training)
        
        print("Staus ticket type------",type(age))
        Cursor.execute("set nocount on;exec SP_UpdateSalesLead %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[name,email,phone,subject,ticket,country,clientarea,potential,city,address,state,zipcode,nationality,profession,dob,income,networth,experience,hear,email2,phone2,country2,noemail,title,hyplinks,appform,age,category,userId,language,training])
        updates=Cursor.fetchone()
        print("Updation done",updates)
     except Exception as e:
                print("Exception------",e)
     finally:
                Cursor.close()






def update_account_client_datails(request):
        update_result=""
        try:
            Cursor=connection.cursor()
            login=int(request.POST.get('formaccountno'))
            
            name=request.POST.get('firstname')
            groups=request.POST.get('groups')
            city=request.POST.get('city')
            address=request.POST.get('address')
            state=request.POST.get('state')
            zipcode=request.POST.get('zipcode')
            country=int(request.POST.get('country'))
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            comment=request.POST.get('comment')
          
            agent=0
            ppassword=request.POST.get('ppassword')
            leverage=0
            taxrate=0
            tinno=request.POST.get('tinno')
            enabled=0
            sendreports=0
            city=request.POST.get('city')
            readonly=0
            changepwd=0
            zipcode=request.POST.get('zipcode')
            
            if zipcode=="":
                zipcode=0
            else:
                zipcode=int(zipcode)
           
            rdcomment=request.POST.get('rdcomment')
            terminated=0
            id=None
            termincomment=request.POST.get('termincomment')
            red=0
            green=0
            blue=0
            color=0
            mothername=request.POST.get('mothername')
            nationality=0
            language=int(request.POST.get('language'))
            created=0
            dob=request.POST.get('dob')
            if(dob==""):
                dob=None
            income=request.POST.get('income')
            
            if income:
                income=int(income)
            else:
                income=None
           
            worth=0
            profession=request.POST.get('profession')
            email2=request.POST.get('email2')
            city=request.POST.get('city')
            phone2=request.POST.get('phone2')
            country2=0
            title=request.POST.get('title')
            userId=request.session.get('UserId')
          
            userId=int(request.session.get('UserId'))
            
            ticket=request.POST.get('formticket')
            subject=request.POST.get('subject')
            clientarea=request.POST.get('clientare')
            potential=0
            exp=int(request.POST.get('experience'))
            
            hear=request.POST.get('hear')
            noemail=0
            hyplink=request.POST.get('hyplink')
            appform=request.POST.get('appform')
            age=request.POST.get('age')
            category=request.POST.get('category')
            scomments=request.POST.get('comments')
            print("login,name,groups,country,city,zipcode,address,phone,email,comment,id,agent,ppassword,leverage,state,taxrate,tinno,enabled,sendreports,readonly,changepwd,rdcomment,terminated,termincomment,red,green,blue,color,mothername,nationality,language,created,dob,income,worth,profession,email2,phone2,country2,title,userId,ticket,subject,clientarea,potential,exp,hear,noemail,hyplink,appform,age,category,scomments")
            print(login,name,groups,country,city,zipcode,address,phone,email,comment,id,agent,ppassword,leverage,state,taxrate,tinno,enabled,sendreports,readonly,changepwd,rdcomment,terminated,termincomment,red,green,blue,color,mothername,nationality,language,created,dob,income,worth,profession,email2,phone2,country2,title,userId,ticket,subject,clientarea,potential,exp,hear,noemail,hyplink,appform,age,category,scomments)
            Cursor.execute("set nocount on;exec SP_UpdateClientDetailsSales %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[login,name,groups,country,city,zipcode,address,phone,email,comment,id,agent,ppassword,leverage,state,taxrate,tinno,enabled,sendreports,readonly,changepwd,rdcomment,terminated,termincomment,red,green,blue,color,mothername,nationality,language,created,dob,income,worth,profession,email2,phone2,country2,title,userId,ticket,subject,clientarea,potential,exp,hear,noemail,hyplink,appform,age,category,scomments])
            update_result=Cursor.fetchone()
            print("Update result====",update_result)
            if update_result:
                update_result=update_result[0]
            print("After update========",update_result)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return update_result




        
    
    












        


