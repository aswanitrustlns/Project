from audioop import reverse
from cmath import log
from email.message import Message

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
            Cursor.execute("SELECT UserName FROM tbl_User where UserID=%s",[userId])
            UserName=Cursor.fetchone()
            UserName=UserName[0]            
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return UserName
    
    # Get Notification
    def get_notification_data(self,userId):
        try:
            Cursor=connection.cursor()
            Cursor.execute("exec SP_GetSummaryToday  %s",[userId])
            notifications = Cursor.fetchall()
            
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
    def get_new_accounts_count(self):
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",["1900-01-01","2022-09-03"])
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
           print("Length of dat======================",len(live_accounts))  
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        for index, item in enumerate(live_accounts):
                itemlist = list(item)
                dt=itemlist[0]
                
                itemlist[0]=datetime.strptime(dt, '%Y-%m-%d').date()
                
               

                live_accounts[index] = tuple(itemlist)
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

    def mailSend(self,token,subject,bcc,cc):
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
                "sender":client_details[3],
                "date":meeting_details[0],
                "time":meeting_details[1],
                "location":meeting_details[2],
                "purpose":meeting_details[3]
            }
            email_template_render=render_to_string("email/MeetingReminder.html",template_data)
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

    #Open demo account
    def open_demo_account(self,title,name,email,phone,country):
        #call dll function
        password=random_ped_gen()
        emailservice.demo_account_email(title,name,password)

    



    def resolve_ticket(self,ticket,userid):
        livestatus=""
        msg=""
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetAccountStatusByTicket %s",[ticket])
           ticket_status=Cursor.fetchone()
           if(ticket_status):
             ticket_status=ticket_status[0]
           if(ticket_status=="Live"):
                msg="Cannot resolve ticket with Account No"
           else:
                value=Cursor.execute("set nocount on;exec SP_ResolveTicket %s,%s,%s",[ticket,userid,"Resolved"])
                if(value==0):
                    msg="'Ticket Resolved Successfully"
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return msg
    
    def get_mail_inbox(self):
        inbox_list=[]
        
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
                res, msg = mail.fetch(str(i), '(RFC822)')
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject=msg["subject"]
                        sender=msg["from"]
                        received_tym=msg["date"]
                        received_tym=received_tym[0:16]
                        # received_tym=datetime.strptime(received_tym,'%d%m%y')
                        # print("Received date===========",type(received_tym))
                        
                        inbox_data=(subject,sender,received_tym,msg["Message-ID"])
                        inbox_list.append(inbox_data)

            
            
        except Exception as e:
            print("Exception------",e)
        finally:
            pass
        inbox_list.reverse()
     
        return inbox_count,inbox_list
    
   

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
#Get activities log    
    def get_activity_log(self,ticket):

        try:
            

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            Cursor=connection.cursor()
            ticket=ticket.strip()
            print("Ticket----------------------------------activity",ticket,current_time)
            Cursor.execute("set nocount on;exec SP_GetTicketLogs %s,%s",[ticket,current_time])
            activity_log=Cursor.fetchall()
            print("Activity log-----------------------------------",activity_log)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return activity_log

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

#send meeting confirmation mail

    def send_meeting_mail(self):
        pass

#cancel meeting mail
    def cancel_meeting_mail(self):
        pass
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
            print("Lead Score-----",lead_score)
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
            print("Lead Score-----",ticket_summary)
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
            print("Lead Score-----",sales_summary)
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
            print("Lead details-----------------",lead_details)
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
            print("Lead Score-----",activity_logs)
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
    def account_status_check_update(self,accountno,request):
        msg=""
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetAccountStatus %s",[accountno])
            status=Cursor.fetchone()
            if(status=="Live" or status=="ReadOnly"):
                msg="You dont have permission to update live account details"
                print("You dont have permission to update live account details")
            else:
               update_result=update_account_client_datails(request)

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
                msg="You dont have permission to update live account details"
                print("You dont have permission to update live account details")
            else:
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
        
    def save_reminder(self,userid,ticket,subject,date,time,badge):
        print("Selcetor saveeeee")
        try:
            desc=""
            rdate=""
            color=""
            login=0
            Cursor=connection.cursor()
            newdate=datetime.strptime(date,'%Y-%m-%d')
            Cursor.execute("set nocount on;exec SP_SetReminder %s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[userid,subject,desc,ticket,newdate,time,rdate,color,login,badge])
            fulltime=date+" "+time
            apdate=datetime.strptime(fulltime,'%Y-%m-%d %H:%M')
            
            print("Date==========================================",apdate)
            Cursor.execute("SELECT email FROM tbl_User where UserID=%s",[userid])
            email=Cursor.fetchone()
            
            outlook = win32com.client.Dispatch("Outlook.Application")
            apdate=apdate.strftime("%Y-%m-%d %H:%M")
            appt = outlook.CreateItem(1) # AppointmentItem
            appt.Start = apdate # yyyy-MM-dd hh:mm
            appt.Subject = "Meeting Test"
            appt.Duration = 60 # In minutes (60 Minutes)
            appt.Location = "Dubai"
            appt.ReminderSet = True
            appt.MeetingStatus = 1 # 1 - olMeeting; Changing the appointment to meeting. Only after changing the meeting status recipients can be added
            appt.Recipients.Add(email) # Don't end ; as delimiter

            appt.Save()
            appt.Send()
            print("Otlook reminder send")
            Cursor.execute("set nocount on;exec SP_InsertTicketLogs %s,%s,%s,%s",[login,badge,"",ticket])
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()

    def get_sticky_text(self,ticket):
            try:
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




def update_ticket(request):
         
     try:
        Cursor=connection.cursor()
        name=request.POST.get('firstname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        subject=request.POST.get('subject')
        ticket=request.POST.get('ticket')
        country=request.POST.get('country')
        clientarea=request.POST.get('clientarea')
        potential=request.POST.get('potential')
        city=request.POST.get('city')
        address=request.POST.get('address')
        state=request.POST.get('state')
        zipcode=request.POST.get('zipcode')
        nationality=request.POST.get('nationality')
        profession=request.POST.get('profession')
        dob=request.POST.get('dob')
        income=request.POST.get('income')
        networth=request.POST.get('networth')
        experience=request.POST.get('experience')
        hear=request.POST.get('hearfrom')
        email2=request.POST.get('email2')
        phone2=request.POST.get('phone2')
        country2=request.POST.get('country2')
        noemail=request.POST.get('noemail')
        title=request.POST.get('title')
        hyplinks=request.POST.get('hyplinks')
        appform=request.POST.get('appform')
        age=request.POST.get('age')
        category=request.POST.get('category')
        userId=request.session.get('UserId')
        language=request.POST.get('language')
        training=request.POST.get('training')
        print("Staus ticket update------",name,email,phone,subject,ticket,country,clientarea,potential,city,address,state,zipcode,nationality,profession,dob,income,networth,experience,hear,email2,phone2,country2,noemail,title,hyplinks,appform,age,category,userId,language,training)
        print("Staus ticket type------",type(name),email,phone,subject,ticket,type(country),clientarea,type(potential),city,address,state,zipcode,type(nationality),profession,dob,type(income),type(networth),type(experience),hear,email2,phone2,type(country2),type(noemail),title,hyplinks,type(appform),type(age),category,userId,language,training)
        Cursor.execute("set nocount on;exec SP_UpdateSalesLead %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[name,email,phone,subject,ticket,country,clientarea,potential,city,address,state,zipcode,nationality,profession,dob,income,networth,experience,hear,email2,phone2,country2,noemail,title,hyplinks,appform,age,category,userId,language,training])
     except Exception as e:
                print("Exception------",e)
     finally:
                Cursor.close()






def update_account_client_datails(self,request):
        
        try:
            Cursor=connection.cursor()
            login=request.POST.get('login')
            name=request.POST.get('name')
            groups=request.POST.get('groups')
            city=request.POST.get('city')
            address=request.POST.get('address')
            state=request.POST.get('state')
            zipcode=request.POST.get('zipcode')
            country=request.POST.get('country')
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            comment=request.POST.get('comment')
            id=request.POST.get('id')
            agent=request.POST.get('agent')
            ppassword=request.POST.get('ppassword')
            leverage=request.POST.get('leverage')
            taxrate=request.POST.get('taxrate')
            tinno=request.POST.get('tinno')
            enabled=request.POST.get('enabled')
            sendreports=request.POST.get('reports')
            city=request.POST.get('city')
            readonly=request.POST.get('readonly')
            changepwd=request.POST.get('changepwd')
            zipcode=request.POST.get('zipcode')
            rdcomment=request.POST.get('rdcomment')
            terminated=request.POST.get('terminated')
            termincomment=request.POST.get('termincomment')
            red=request.POST.get('red')
            green=request.POST.get('green')
            blue=request.POST.get('blue')
            color=request.POST.get('color')
            mothername=request.POST.get('mothername')
            nationality=request.POST.get('nationality')
            language=request.POST.get('language')
            created=request.POST.get('created')
            dob=request.POST.get('dob')
            income=request.POST.get('income')
            worth=request.POST.get('worth')
            profession=request.POST.get('profession')
            email2=request.POST.get('email2')
            city=request.POST.get('city')
            phone2=request.POST.get('phone2')
            country2=request.POST.get('country2')
            title=request.POST.get('title')
            userId=request.POST.get('UserId')
            ticket=request.POST.get('ticket')
            subject=request.POST.get('subject')
            clientarea=request.POST.get('clientare')
            potential=request.POST.get('potential')
            exp=request.POST.get('exp')
            hear=request.POST.get('hear')
            noemail=request.POST.get('noemail')
            hyplink=request.POST.get('hyplink')
            appform=request.POST.get('appform')
            age=request.POST.get('age')
            category=request.POST.get('category')
            scomments=request.POST.get('comments')
            update_result=Cursor.execute("set nocount on;exec SP_UpdateSalesLead %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[login,name,groups,country,city,zipcode,address,phone,email,comment,id,agent,ppassword,leverage,state,taxrate,tinno,enabled,sendreports,readonly,changepwd,rdcomment,terminated,termincomment,red,green,blue,color,mothername,nationality,language,created,dob,income,worth,profession,email2,phone2,country2,title,userId,ticket,subject,clientarea,potential,exp,hear,noemail,hyplink,appform,age,category,scomments])
        
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return update_result




        
    
    












        


