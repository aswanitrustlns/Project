from audioop import reverse
from cmath import log
from email.message import Message
from django.db import connection
from datetime import datetime, timedelta
from ctypes import *
import subprocess
import win32com.client
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
import imaplib
import email
import html2text

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
            #receiver=client_details[2]
            receiver='aswani.trustlns@gmail.com'

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
    #     except Exception as e:
    #         print("Exception------",e)
    #     finally:
    #         Cursor.close()
    #     return leads_details

    #Open demo account
    def open_demo_account(self):
        pass
    
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
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLeadScore %s",[ticket])
            lead_score=Cursor.fetchall()
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
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLeadDetailsByTicket %s,%s",[ticket,userid])
            lead_details=Cursor.fetchone()
            print("Lead details-----------------",lead_details)
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
    
    












        


