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
from .models import TblClients,TblEwalletTransaction
from django.db.models import OuterRef, Subquery,Max,Q
from django.core import serializers
from django.conf import settings
import imaplib
import email
import html2text
import os
import json
from .emailservices import EmailServices
from django.core.serializers.json import DjangoJSONEncoder

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
            mailInfo=UserData[1]  
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
            while (Cursor.nextset()):
                notification_count = Cursor.fetchall()                
                notify_count=notification_count[0]
                notification_count=notify_count[0]
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
            Cursor.execute("SELECT ID,Country,Code FROM tbl_Country")
            country_list=Cursor.fetchall()
            
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return country_list
    #Load nationality
    def load_nationality(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetNationality") 
            nationality=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return nationality
    #Load Country
    def loadCountry(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetSalesLeadCountry") 
            all_country=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return all_country
    #Load Risk category
    def loadRiskCategory(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetRiskCategory") 
            risk_category=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return risk_category
    #Load Leverage
    def loadLeverage(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetLeverage") 
            leverage=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return leverage
    #Load Account Types
    def loadAccountType(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetAccountTypes") 
            account_type=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return account_type


    def loadgroups(self,user,server,password):
        try:
            
            hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
            GetGroups = hllDll.GetGroups_withLP
            hllDll.GetGroups_withLP.argtype = c_char_p,c_int,c_char_p
            hllDll.GetGroups_withLP.restype = POINTER(c_char_p)
            username=int(user)
            login = c_int(username)
            groups=GetGroups(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value)
            resul=string_at(groups)
            dataset=str(resul, 'utf-8')
            
            if(len(dataset)!=0):  
                dataset=dataset.split(",")              
                output_str=dataset
                output_str=' '.join(output_str).split()
            else:
                output_str =""    
            
            print("Data set======",output_str)
        except Exception as e:
            print("Exception------",e)
        
        return output_str
    #Load account type category
    def loadAccountCategory(self,acno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetAccTypeClientCategory %s",[acno]) 
            account_category=Cursor.fetchall()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return account_category

    def dll_get_groups(self,user,server,password):
       
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetGroups = hllDll.GetGroups_withLP
        hllDll.GetGroups_withLP.argtype = c_char_p,c_int,c_char_p
        hllDll.GetGroups_withLP.restype = POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        groups=GetGroups(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value)
        resul=string_at(groups)
        dataset=str(resul, 'utf-8')
        if(len(dataset)!=0):                
            output_str=dataset
        else:
            output_str =""    
        return output_str


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
                Cursor.execute("SET NOCOUNT ON;exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",[from_date,to_date,'',0,0,'',1])
                leads_data=Cursor.fetchall() 
            else:
                from_date=date_yesterday
                to_date=date_today
                Cursor.execute("SET NOCOUNT ON;exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",[from_date,to_date,'',0,0,'',1])
                leads_data=Cursor.fetchall()
                
               
            # for index, item in enumerate(leads_data):
            #     itemlist = list(item)
            #     dt=itemlist[0]
                
            #     itemlist[0]=datetime.strptime(dt, '%Y-%m-%d').date()
                
               

            #     leads_data[index] = tuple(itemlist)
          
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return leads_data,leads_count,from_date,to_date,
    #Get Lead Page click
    def get_leads_clicks(self,status,count):
        try:
            leads_data=[]
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_LeadsListing_PY %s,%s",[status,count])
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
                
                           
            if(ticket=="spoken"):
                print("Load spoken")            
                Cursor.execute("exec SP_GetSpokenLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,date_yesterday,date_today,'P',0])
                _tickets=Cursor.fetchall()
            if(ticket=="resolved"):
                print("Load resolved")            
                Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,date_yesterday,date_today,'R',0])
                _tickets=Cursor.fetchall()
            if(ticket=="dormant"):
                date_yesterday=""
                date_today=""
                print("dormant tickets")
                Cursor.execute("exec SP_GetDormantSalesLeadsPaginate_PY %s,%s,%s",[userId,"P",userId])
                _tickets=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        
        return _tickets,date_yesterday,date_today
    
    #Get Tickets for summary
    def get_tickets_summary(self,userId,summary,status):
        try:
            tickets=""
            print("Summary=====")
            Cursor=connection.cursor()  
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            fromdate="1900-09-19"
            if status=="Pending":
                Cursor.execute("set nocount on;exec SP_GetSalesLeadsListPaginateByCount %s,%s,%s,%s",[userId,"1900-09-19",date_today,summary])
                tickets=Cursor.fetchall()
            if status=="Resolved":
                print("Status====",status)
                Cursor.execute("set nocount on;exec SP_GetResolvedTicketsPaginateByCount %s,%s,%s,%s",[userId,"1900-09-19",date_today,summary])
                tickets=Cursor.fetchall()
            if status=="Dormant":
                
                Cursor.execute("set nocount on;exec SP_GetDormantTicketsPaginateByCount %s,%s,%s,%s",[userId,"1900-09-19",date_today,summary])
                tickets=Cursor.fetchall()

        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return tickets,fromdate,date_today
        

    def get_all_tickets(self,userId,status,from_date,to_date,repId,source):
        try:
            _tickets=[]
            
            Cursor=connection.cursor()
            
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                    date_yesterday = datetime.today()-timedelta(3)
            else:
                date_yesterday = datetime.today()-timedelta(1)
                    
            date_yesterday=date_yesterday.strftime("%Y-%m-%d") 
            if ((from_date=="")and(to_date=="")):      
                from_date=date_yesterday
                to_date=date_today            
            if status=="D":
                Cursor.execute("exec SP_GetDormantSalesLeadsPaginate_PY %s,%s,%s",[userId,"P",userId])
                _tickets=Cursor.fetchall()
            else:
                     print("Inputs========",userId,from_date,to_date,status,repId,source)
                     Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[userId,from_date,to_date,status,repId,0,"",source,0,1])
                     _tickets=Cursor.fetchall()
            # if(ticket=="resolved"):
               
            #     print("Load all resolved")
            #     Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,from_date,to_date,'R',0])
            #     _tickets=Cursor.fetchall()
            
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close() 
        return _tickets,from_date,to_date

    #Get new accounts count
    def get_new_accounts_count(self,from_date,to_date):
        try:
            
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec SP_GetNewAccountsCount %s,%s",[from_date,to_date])
           accounts_count=Cursor.fetchone()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        
        return accounts_count
     #Get new accounts count for variants
    # def get_new_accounts_count_variants(self,from_date,to_date,change):
    #     try:
            
    #        Cursor=connection.cursor()
    #        Cursor.execute("set nocount on;exec SP_GetNewAccountsListing  %s,%s,%s",[from_date,to_date,change])
    #        accounts_count=Cursor.fetchone()
    #     except Exception as e:
    #         print("Exception---",e)
    #     finally:
    #         Cursor.close()
        
    #     return accounts_count
    
    # Get New Accounts page data
    def get_new_accounts(self,change,status,from_date,to_date):
        try:
           live_accounts=""
           Cursor=connection.cursor()
           date_today=datetime.today().date()    
           date_today=date_today.strftime("%Y-%m-%d")
           week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
           
           if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
           else:
                date_yesterday = datetime.today()-timedelta(1)
           date_yesterday=date_yesterday.strftime("%Y-%m-%d")
           print("Change and status====",change,status,date_yesterday,date_today)
           if(change == "All"):
                
                Cursor.execute("set nocount on;exec SP_GetNewAccountsListing %s,%s,%s",[from_date,to_date,status])  
                live_accounts=Cursor.fetchall()
           else: 
                
                Cursor.execute("set nocount on;exec SP_GetNewAccountsListing %s,%s,%s",[date_yesterday,date_today,change])   #exec SP_GetNewAccountsListing
                live_accounts=Cursor.fetchall()
           
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return live_accounts

     # Get New Accounts click data
    def get_new_accounts_click(self,status,from_date,to_date):
        try:
           Cursor=connection.cursor()
           print("Status=====",status)
           Cursor.execute("set nocount on;exec SP_GetNewAccountsListing %s,%s,%s",[from_date,to_date,status])  
           live_accounts=Cursor.fetchall()
          
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return live_accounts    
   # Get New Accounts page data
    # def get_new_accounts_filter(self,change):
    #     try:
    #        Cursor=connection.cursor()
    #        date_today=datetime.today().date()    
    #        date_today=date_today.strftime("%Y-%m-%d")
    #        week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
    #        if(week_day==0):
    #             date_yesterday = datetime.today()-timedelta(3)
    #        else:
    #             date_yesterday = datetime.today()-timedelta(1)

    #        date_yesterday=date_yesterday.strftime("%Y-%m-%d")
    #        Cursor.execute("set nocount on;exec SP_GetNewActsFromDashboard %s,%s,%s",[date_yesterday,date_today,change])  
    #        live_accounts=Cursor.fetchall()
         
    #     except Exception as e:
    #         print("Exception---",e)
    #     finally:
    #         Cursor.close()
     
    #     return live_accounts
#Get new Accounts weekly filter
    def get_new_accounts_weekly_filter(self,change,date_from,date_to):
        try:
           live_accounts=""
           Cursor=connection.cursor()
           print("Data====================================",date_from,date_to,change)
           Cursor.execute("set nocount on;exec SP_GetNewActsFromDashboard %s,%s,%s",[date_from,date_to,change])  
           live_accounts=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return live_accounts
        
#Duplicate lead check
    def check_duplicate(self,phone,email):
        try:
           Cursor=connection.cursor()
           Cursor.execute("set nocount on;exec TC_GetDuplicatePhoneList %s,%s",[phone,email])
           duplicate=Cursor.fetchall()
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
           print("New created ticket===",ticket_data)
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
            email_from = 'cs@trustcapital.com '
            receiver=client_details[2]
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
            subject="Trust Capital - Meeting Cancelled"
            email_from = settings.EMAIL_HOST_USER
            receiver=client_details[2]
            #receiver='aswani.technology@gmail.com'
            template_data={
                "title":client_details[0],
                "name":client_details[1],
                "sender":client_details[3],
                
            }
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
    def open_demo_account(self,user,server,password,title,name,email,phone,country):
        #call dll function
        try:
            Cursor=connection.cursor()
            Cursor.execute("SELECT COUNTRY FROM tbl_Country where ID=%s",[country])
            country_name=Cursor.fetchone()
            if (country_name):
                country_name=country_name[0]
        
            passwordgen=random_ped_gen()
            demo_account=dll_demo_account(user,server,password,name,email,phone,country_name,passwordgen)
            if(demo_account != 0):
                emailservice.demo_account_email(title,name,demo_account,passwordgen,email)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()

    



    def resolve_ticket(self,ticket,userid,reason):
        livestatus=""
        msg="Ticket Resolved"
        try:
           Cursor=connection.cursor()
           
           Cursor.execute("set nocount on;exec SP_GetAccountStatusByTicket %s",[ticket])
           ticket_status=Cursor.fetchone()
           
           if(ticket_status):
                ticket_status=ticket_status[0]
                if(ticket_status=="Live"):
                        msg="Cannot resolve ticket with Account No"
           else:
                        Cursor.execute("set nocount on;exec SP_ResolveTicket %s,%s,%s",[ticket,userid,reason])
                        value=Cursor.fetchone()
                        if value:
                            value=value[0]
                            if(value==0):
                                msg="Ticket Resolved Successfully"
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
           
            mail = imaplib.IMAP4_SSL(host=settings.EMAIL_HOST)

            mail.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
            status, messages=mail.select("INBOX")
            _, selected_mails = mail.search(None,'(ALL)')
            inbox_count=len(selected_mails[0].split())
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
                        inbox_list.append(inbox_data)
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
            
            type, selected_mails = mailbox.search(None,search_cr) #mail.search based criteria mail.search(None,'(FROM "email" SUBJECT "the subject" UNSEEN)')
            count=len(selected_mails[0].split())
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

    #Email template send items from backoffice----
    def template_send_items_backoffice_list(self,emailname):
        count=0
        try:
            inbox_list=[]
            username="backoffice@trustcapital.com "
            app_password="n59K3x_p"
            
            mail_server = 'mail.trusttc.com'

            mailbox = imaplib.IMAP4_SSL(mail_server)

            mailbox.login(username, app_password)
            mailbox.select("INBOX")
            search_cr='(TO "'+emailname+'")'
            
            type, selected_mails = mailbox.search(None,search_cr) #mail.search based criteria mail.search(None,'(FROM "email" SUBJECT "the subject" UNSEEN)')
            count=len(selected_mails[0].split())
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
    #Email template send items from sales----
    def template_send_items_sales_list(self,emailname):
        count=0
        try:
            inbox_list=[]
            username="sales@trustcapital.com"
            app_password="Sa1936bb2k"

            mail_server = 'mail.trusttc.com'

            mailbox = imaplib.IMAP4_SSL(mail_server)

            mailbox.login(username, app_password)
            mailbox.select("INBOX")
            search_cr='(TO "'+emailname+'")'
            
            type, selected_mails = mailbox.search(None,search_cr) #mail.search based criteria mail.search(None,'(FROM "email" SUBJECT "the subject" UNSEEN)')
            count=len(selected_mails[0].split())
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
    #Email template send items from support----
    def template_send_items_support_list(self,emailname):
        count=0
        try:
            inbox_list=[]
            username="support@truscapital.com"
            app_password="zvXi98_9"

            mail_server = 'mail.trusttc.com'

            mailbox = imaplib.IMAP4_SSL(mail_server)

            mailbox.login(username, app_password)
            mailbox.select("INBOX")
            search_cr='(TO "'+emailname+'")'
            
            type, selected_mails = mailbox.search(None,search_cr) #mail.search based criteria mail.search(None,'(FROM "email" SUBJECT "the subject" UNSEEN)')
            count=len(selected_mails[0].split())
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
    def read_mail_senditems(self,emailname,message,username,app_password):
       
        multipart="false"
        
        mail_server = 'mail.trusttc.com'
        mail = imaplib.IMAP4_SSL(mail_server)
        message_data=""
        subject=""
        sender=""
        mail.login(username, app_password)
        status, messages=mail.select("INBOX")
        search_cr='(TO "'+emailname+'")'
        elem, selected_mails = mail.search(None,search_cr)
        if os.path.isfile("templates\\test\\index.html"):
            os.remove("templates\\test\\index.html")
       
        for i in selected_mails[0].split():
            res, msg = mail.fetch(i, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    if(message == msg["Message-ID"]):
                        print("Message")
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        if msg.is_multipart():
                            
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                
                                content_disposition = str(part.get("Content-Disposition"))
            
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8')
                                except:
                                    pass
            
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    message_data=body
                                    print(body)
                                if content_type == "text/html":
                                    multipart="true"
                                    open_html(body)
                                elif "attachment" in content_disposition:
                                    # download_attachment(part)
                                    print("Attachment is there")
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":                                    
                                    
                                    message = part.get_payload(decode=True)                                    
                                    message_data=message.decode()                                      
                                    break
                                
                                if part.get_content_type()=="text/html":                                    
                                    multipart="true"
                                    body = part.get_payload(decode=True).decode()
                                    open_html(body)
                                
                            
        
        return message_data,subject,sender,multipart

# Send Items for manage tickets
    def read_mail_senditems_backoffice(self,emailname,message):
       
        multipart="false"
        username="backoffice@trustcapital.com"
        app_password="WmY&SF9sX8kv"
        mail_server = 'n59K3x_p'
        mail = imaplib.IMAP4_SSL(mail_server)
        message_data=""
        subject=""
        sender=""
        mail.login(username, app_password)
        status, messages=mail.select("INBOX")
        search_cr='(TO "'+emailname+'")'
        elem, selected_mails = mail.search(None,search_cr)
        if os.path.isfile("templates\\test\\index.html"):
            os.remove("templates\\test\\index.html")
       
        for i in selected_mails[0].split():
            res, msg = mail.fetch(i, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    if(message == msg["Message-ID"]):
                        print("Message")
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        if msg.is_multipart():
                            
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                
                                content_disposition = str(part.get("Content-Disposition"))
            
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8')
                                except:
                                    pass
            
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    message_data=body
                                    print(body)
                                if content_type == "text/html":
                                    multipart="true"
                                    open_html(body)
                                elif "attachment" in content_disposition:
                                    # download_attachment(part)
                                    print("Attachment is there")
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":                                    
                                    
                                    message = part.get_payload(decode=True)                                    
                                    message_data=message.decode()                                      
                                    break
                                
                                if part.get_content_type()=="text/html":                                    
                                    multipart="true"
                                    body = part.get_payload(decode=True).decode()
                                    open_html(body)
                                
                            
        
        return message_data,subject,sender,multipart
    # Send Items for manage tickets
    def read_mail_senditems_sales(self,emailname,message):
       
        multipart="false"
        username="sales@trustcapital.com"
        app_password="Sa1936bb2k"
        mail_server = 'mail.trusttc.com'
        mail = imaplib.IMAP4_SSL(mail_server)
        message_data=""
        subject=""
        sender=""
        mail.login(username, app_password)
        status, messages=mail.select("INBOX")
        search_cr='(TO "'+emailname+'")'
        elem, selected_mails = mail.search(None,search_cr)
        if os.path.isfile("templates\\test\\index.html"):
            os.remove("templates\\test\\index.html")
       
        for i in selected_mails[0].split():
            res, msg = mail.fetch(i, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    if(message == msg["Message-ID"]):
                        print("Message")
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        if msg.is_multipart():
                            
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                
                                content_disposition = str(part.get("Content-Disposition"))
            
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8')
                                except:
                                    pass
            
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    message_data=body
                                    print(body)
                                if content_type == "text/html":
                                    multipart="true"
                                    open_html(body)
                                elif "attachment" in content_disposition:
                                    # download_attachment(part)
                                    print("Attachment is there")
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":                                    
                                    
                                    message = part.get_payload(decode=True)                                    
                                    message_data=message.decode()                                      
                                    break
                                
                                if part.get_content_type()=="text/html":                                    
                                    multipart="true"
                                    body = part.get_payload(decode=True).decode()
                                    open_html(body)
                                
                            
        
        return message_data,subject,sender,multipart
    # Send Items for manage tickets
    def read_mail_senditems_support(self,emailname,message):
       
        multipart="false"
        username="support@trustcapital.com"
        app_password="zxXi98_9"
        mail_server = 'mail.trusttc.com'
        mail = imaplib.IMAP4_SSL(mail_server)
        message_data=""
        subject=""
        sender=""
        mail.login(username, app_password)
        status, messages=mail.select("INBOX")
        search_cr='(TO "'+emailname+'")'
        elem, selected_mails = mail.search(None,search_cr)
        if os.path.isfile("templates\\test\\index.html"):
            os.remove("templates\\test\\index.html")
       
        for i in selected_mails[0].split():
            res, msg = mail.fetch(i, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    if(message == msg["Message-ID"]):
                        print("Message")
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        if msg.is_multipart():
                            
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                
                                content_disposition = str(part.get("Content-Disposition"))
            
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8')
                                except:
                                    pass
            
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    message_data=body
                                    print(body)
                                if content_type == "text/html":
                                    multipart="true"
                                    open_html(body)
                                elif "attachment" in content_disposition:
                                    # download_attachment(part)
                                    print("Attachment is there")
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":                                    
                                    
                                    message = part.get_payload(decode=True)                                    
                                    message_data=message.decode()                                      
                                    break
                                
                                if part.get_content_type()=="text/html":                                    
                                    multipart="true"
                                    body = part.get_payload(decode=True).decode()
                                    open_html(body)
                                
                            
        
        return message_data,subject,sender,multipart

 # Read mail inbox
    def read_mail_inbox(self,message):
        multipart="false"
        print("read mail inboxxxx",message)
        mail = imaplib.IMAP4_SSL(host=settings.EMAIL_HOST)
        message_data=""
        subject=""
        sender=""
        mail.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        status, messages=mail.select("INBOX")
        _, selected_mails = mail.search(None,'(ALL)')
        inbox_count=len(selected_mails[0].split())
        if os.path.isfile("templates\\test\\index.html"):
            os.remove("templates\\test\\index.html")

        for i in selected_mails[0].split():
            res, msg = mail.fetch(i, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    if(message == msg["Message-ID"]):
                        
                        subject=msg["subject"]
                        sender=msg["from"]
                        content_type=msg["content-type"]
                        
                        if(content_type=="text/html"):
                            message_data=message.decode('utf-8')
                            message_data=get_template(message_data)
                        if(content_type=="text/plain"):
                            
                            message_data=message.decode('utf-8')
                        if msg.is_multipart():
                            
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                
                                content_disposition = str(part.get("Content-Disposition"))
            
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8')
                                except:
                                    pass
            
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    message_data=body
                                  
                                if content_type == "text/html":
                                    multipart="true"
                                    open_html(body)
                                elif "attachment" in content_disposition:
                                    # download_attachment(part)
                                    print("Attachment is there")
                           
                        else:
                            for part in msg.walk():
                            
                                if part.get_content_type()=="text/plain":                                    
                                    
                                    message = part.get_payload(decode=True)                                    
                                    message_data=message.decode()                                      
                                    break
                                
                                if part.get_content_type()=="text/html":                                    
                                    multipart="true"
                                    body = part.get_payload(decode=True).decode()
                                    open_html(body)
                                    # text = f"{part.get_payload(decode=True)}"
                                    # html = text.replace("b'", "")
                                    # h = html2text.HTML2Text()
                                    # h.body_width = 0
                                    # h.ignore_links = True                                 
                                    # output = (h.handle(f'''{html}''').replace("\\t", " "))
                                    # output = output.replace("\\n", " ")
                                    # output = output.replace("\\r", " ")
                                    # output = output.replace("'", "")
                                    # output = output.replace("\\", "")
                                    # output = output.replace("---", "")
                                    # output = output.replace("|", "")
                                    # print("Outpu----------------",output)
                                    # message_data=output
                                
                            
        
        return message_data,subject,sender,inbox_count,multipart
    

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
            Cursor.execute("set nocount on;exec SP_GetLeadDetailsByTicket_PY %s,%s",[ticket,userid])
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
            
            if(status=="Live" or status=="ReadOnly"):
                msg="You dont have permission to update live account details"
                
            else:
            #    update_result=update_account_client_datails(request)
               update_result=update_ticket(request) 
               emailservice.account_update_email(accountno,ticket,request,update_result)
               msg="Updated Successfully"
               if(update_result!=None):
                    pass
               
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
        
    def save_reminder(self,userid,ticket,subject,date,time,login,color,mail,flag):
        
        try:
            subject="Reminder set for Ticket "+ticket+" on "+date+" at "+time
            badge="Green"
            desc=subject
            rdate=datetime.today().date()
            if login=="":
                login=0
            Cursor=connection.cursor()
            date_today=datetime.today().date()  
            Cursor.execute("set nocount on;exec SP_SetReminder %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[userid,subject,desc,ticket,date,time,rdate,color,login,badge,flag])
            fulltime=date+" "+time
            apdate=datetime.strptime(fulltime,'%Y-%m-%d %H:%M')
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
            Cursor.execute("set nocount on;exec SP_InsertTicketLogs %s,%s,%s,%s",[userid,logdata,logtype,ticket])
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
    #Get sales rep permission
    def get_salesrep_permission(self,userId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetSalesRepPermission  %s",[userId]) 
            permission=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return permission
    #Get sales call report
    def get_sales_call_report(self,from_date,to_date,salesRep):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec TC_GetSalesCallReport  %s,%s,%s",[from_date,to_date,salesRep]) 
            call_report=Cursor.fetchall()
            Cursor.execute("set nocount on;exec Sp_Interested  %s,%s,%s",[from_date,to_date,salesRep]) 
            interested=Cursor.fetchall()
            if interested:
                interested=interested[0]
                interested=interested[0]
            print("Interested=======",interested)
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return call_report,interested
      #Get sales call report monthly
    def get_sales_call_report_monthly(self,month,year,salesRep):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec TC_GetSalesCallReportMonthly  %s,%s,%s",[month,year,salesRep]) 
            monthly_report=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return monthly_report
    # Get calendar events
    def get_all_calender_events(self,userId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetAllReminders %s",[userId]) 
            all_reminders=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return all_reminders
    #Load Ticket Reminders
    def load_ticket_reminders(self,userid,ticket):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetTicketReminders %s,%s",[userid,ticket]) 
            all_reminders=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return all_reminders
     #Load Ticket Summary
    def load_ticket_summary_pending(self,userid):
        try:
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_GetPendingTicketsSummary %s",[userid]) 
            pending=Cursor.fetchone()  
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return pending
      #Load Ticket Summary All
    def load_ticket_summary(self,userid):
        try:
            Cursor=connection.cursor()  
            Cursor.execute("set nocount on;exec SP_GetPendingTicketsSummary %s",[userid]) 
            pending=Cursor.fetchone()  
            Cursor.execute("set nocount on;exec SP_GetResolvedTicketsSummary %s",[userid]) 
            resolved=Cursor.fetchone()       
            Cursor.execute("set nocount on;exec SP_GetDormantTicketsSummary %s",[userid]) 
            dormant=Cursor.fetchone()

        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return pending,resolved,dormant
    #Get All Complaints
    def get_all_complaints(self):
        try:
            Cursor=connection.cursor()  
            Cursor.execute("set nocount on;exec SP_GetComplaintsList %s",[21])
            complaints=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return complaints
    #Get Livechat logs
    def get_live_chat_logs(self,fromdate,todate,salesrepid,attendedby):
        try:
            print("Inputs=====",fromdate,todate,salesrepid,attendedby)
            chats=""
            Cursor=connection.cursor()  
            Cursor.execute("set nocount on;exec SP_LiveChatLogs %s,%s,%s,%s",[fromdate,todate,salesrepid,attendedby])
            chats=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return chats

    #Get complaint Id
    def get_complaint_details(self,complaintid):
        try:
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_GetComplaintDetails %s",[complaintid]) 
            details=Cursor.fetchone()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return details
        #Get complaint Id
    def edit_complaint_details(self,complaintid,status,description,userid):
        msg=""
        try:
            msg="Please try again"
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_UpdateComplaint %s,%s,%s,%s",[complaintid,status,description,userid]) 
            msg="Updated Successfully"
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return msg
    #Get source for inactive tickets page
    def get_sources(self):
        try:
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_GetSourceListTicket") 
            sourcelist=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return sourcelist
    #Get inactive Tickets
    def inactive_tickets_default(self,fromdate,todate,repId,source):
        try:
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_GetInactiveTickets %s,%s,%s,%s",[fromdate,todate,source,repId]) 
            inactive=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return inactive
    #Get Campaign titles
    def get_campaigns(self):
        try:
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_GetCampaignTitles") 
            campaigns=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return campaigns
    #Get latest webinar
    def get_latest_seminar(request):
        try:
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_GetSeminarDetailsTitleWithDate") 
            webinars=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return webinars
  

    #Get Live chat salesrep
    def get_livechat_reps(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_getLiveChatSalesRep") 
            livechat_rep=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return livechat_rep
    #Get Live chat Users
    def get_livechat_users(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_getLiveChatUsers") 
            livechat_users=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return livechat_users
    #Get missed chat
    def get_missedchat(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetMissedLiveChat") 
            livechat_users=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return livechat_users

    #Get Campaign Report
    
    def get_campaigns_report(self,campaignid,countryid):
        try:
            Cursor=connection.cursor()
            
            Cursor.execute("set nocount on;exec SP_GetCampaignsReport %s,%s",[campaignid,countryid]) 
            campaign_report=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return campaign_report
    
    #Get funded Today

    def funded_today(self):
        try:
            funded_clients=[]
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(1)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            new_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[date_yesterday,date_today]).exclude(isib=1).values_list('login',flat=True))
            clients_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_today).values('accnt_no').annotate(Max('id'))
            get_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_today.values('id__max')))
            disctinct_today_list=[]
            for id in get_today_id.iterator():
                disctinct_today_list.append(id.id)
            print("Distinct today list====",disctinct_today_list)
            funded_count=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).count()
            nonfunded_count=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).count()
            funded_today_list=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list)
            if funded_today_list:
                funded_clients=TblClients.objects.filter(login__in=funded_today_list)
            
        except Exception as e:
            print("Exception---",e)
        return funded_count,nonfunded_count,funded_clients,date_today,date_yesterday
    
    #Get funded Weekly

    def funded_weekly(self):
        try:
            funded_clients=[]
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(week_day)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            new_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[date_yesterday,date_today]).exclude(isib=1).values_list('login',flat=True))
            clients_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_today).values('accnt_no').annotate(Max('id'))
            get_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_today.values('id__max')))
            disctinct_today_list=[]
            for id in get_today_id.iterator():
                disctinct_today_list.append(id.id)
            print("Distinct today list====",disctinct_today_list)
            funded_count=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).count()
            nonfunded_count=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).count()
            funded_today_list=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list)
            if funded_today_list:
                funded_clients=TblClients.objects.filter(login__in=funded_today_list)
            print("Funded Today------",funded_today_list)
        except Exception as e:
            print("Exception---",e)
        return funded_count,nonfunded_count,funded_clients,date_today,date_yesterday

     #Get nonfunded Weekly

    def nonfunded_weekly(self):
        try:
            funded_clients=[]
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(week_day)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            new_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[date_yesterday,date_today]).exclude(isib=1).values_list('login',flat=True))
            clients_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_today).values('accnt_no').annotate(Max('id'))
            get_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_today.values('id__max')))
            disctinct_today_list=[]
            for id in get_today_id.iterator():
                disctinct_today_list.append(id.id)
            print("Distinct today list====",disctinct_today_list)
            funded_count=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).count()
            nonfunded_count=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).count()
            funded_today_list=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list)
            if funded_today_list:
                funded_clients=TblClients.objects.filter(login__in=funded_today_list)
            print("Funded Today------",funded_today_list)
        except Exception as e:
            print("Exception---",e)
        return funded_count,nonfunded_count,funded_clients,date_today,date_yesterday


      #Get funded by date

    def funded_by_date(self,from_date,to_date):
        try:
            funded_clients=[]
            

            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
           
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(1)
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            if from_date=="":
                from_date=date_yesterday
            if to_date=="":
                to_date=date_today.strftime("%Y-%m-%d")
            
            new_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[from_date,to_date]).exclude(isib=1).values_list('login',flat=True))
            print("New clients today===",new_clients_today)
            clients_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_today).values('accnt_no').annotate(Max('id'))
            get_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_today.values('id__max')))
            disctinct_today_list=[]
            for id in get_today_id.iterator():
                disctinct_today_list.append(id.id)
            print("Distinct today list====",disctinct_today_list)
            funded_count=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).count()
            nonfunded_count=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).count()
            funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).values_list('accnt_no',flat=True))
            print("Funded today list====",funded_today_list)
            if funded_today_list:
                funded_clients=TblClients.objects.filter(login__in=funded_today_list)
                
                
            
        except Exception as e:
            print("Exception---",e)
        return funded_count,nonfunded_count,funded_clients,from_date,to_date
       
    #Get nonfunded by date

    def nonfunded_by_date(self,from_date,todate):
        try:
            funded_clients=[]
            
            new_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[from_date,todate]).exclude(isib=1).values_list('login',flat=True))
            clients_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=new_clients_today).values('accnt_no').annotate(Max('id'))
            get_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(clients_today.values('id__max')))
            disctinct_today_list=[]
            for id in get_today_id.iterator():
                disctinct_today_list.append(id.id)
            print("Distinct today list====",disctinct_today_list)
            funded_count=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_today_list).count()
            nonfunded_count=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).count()
            funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_today_list).values_list('accnt_no',flat=True))
            if funded_today_list:
                funded_clients=TblClients.objects.filter(login__in=funded_today_list)
            print("Funded Today------",funded_today_list)
        except Exception as e:
            print("Exception---",e)
        return funded_count,nonfunded_count,funded_clients,from_date,todate

    #Existing Funded Today
    def existing_funded_today(self):
        try:
            existing_funded_clients=[]
            existing_funded_today_list=[]
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(1)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            one_week=datetime.today()-timedelta(days=7)
            one_week=one_week.strftime("%Y-%m-%d")
            existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))
            existing_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_today).values('accnt_no').annotate(Max('id'))
            get_ext_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(existing_today.values('id__max')))
            disctinct_ext_today_list=[]
            for id in get_ext_today_id.iterator():
                disctinct_ext_today_list.append(id.id)
            existing_funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday,date_today],id__in=disctinct_ext_today_list).values_list('accnt_no',flat=True))
            print("Ext=====",existing_funded_today_list)
            if existing_funded_today_list:
                existing_funded_clients=TblClients.objects.filter(login__in=existing_funded_today_list)
            print("List====",existing_funded_clients)
        except Exception as e:
            print("Exception---",e)
        return existing_funded_clients,date_today,date_yesterday

    def existing_funded_week(self):
        try:
            existing_funded_clients=[]
            existing_funded_today_list=[]
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(week_day)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            one_week=datetime.today()-timedelta(days=7)
            one_week=one_week.strftime("%Y-%m-%d")
            existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))
            existing_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_today).values('accnt_no').annotate(Max('id'))
            get_ext_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(existing_today.values('id__max')))
            disctinct_ext_today_list=[]
            for id in get_ext_today_id.iterator():
                disctinct_ext_today_list.append(id.id)


            # existing_funded_today=TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status=1,trans_date__date__range=[date_yesterday,date_today],id__in=disctinct_ext_today_list).count()
            existing_funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday,date_today],id__in=disctinct_ext_today_list).values_list('accnt_no',flat=True))
            print("Ext=====",existing_funded_today_list)
            existing_funded_clients=TblClients.objects.filter(login__in=existing_funded_today_list)
            print("List====",existing_funded_clients)
        except Exception as e:
            print("Exception---",e)
        return existing_funded_clients,date_today,date_yesterday


    def existing_nonfunded_total(self):
        try:
            existing_funded_today_list=""
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(week_day)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            one_week=datetime.today()-timedelta(days=7)
            one_week=one_week.strftime("%Y-%m-%d")
            existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))
           
            existing_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_today).values('accnt_no').annotate(Max('id'))
            get_ext_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(existing_today.values('id__max')))
            
            disctinct_ext_today_list=[]
            for id in get_ext_today_id.iterator():
                disctinct_ext_today_list.append(id.id)

            print("Existing clinets today====",disctinct_ext_today_list)
            # existing_funded_today=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday,date_today],id__in=disctinct_ext_today_list).count()
            existing_funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_ext_today_list).values_list('accnt_no',flat=True))
            print("Ext=====",existing_funded_today_list)
            existing_funded_clients=TblClients.objects.filter(login__in=existing_funded_today_list)
            print("List====",existing_funded_clients)
        except Exception as e:
            print("Exception---",e)
        return existing_funded_clients,date_today,date_yesterday

    def existing_nonfunded_click(self,fromdate,todate):
        try:
            existing_funded_today_list=""
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(week_day)
            
            
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            one_week=datetime.today()-timedelta(days=7)
            one_week=one_week.strftime("%Y-%m-%d")

            if fromdate=="":
                
                existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))
            else:
                existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[fromdate,todate]).exclude(isib=1).values_list('login',flat=True))
           
            existing_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_today).values('accnt_no').annotate(Max('id'))
            get_ext_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(existing_today.values('id__max')))
            
            disctinct_ext_today_list=[]
            for id in get_ext_today_id.iterator():
                disctinct_ext_today_list.append(id.id)

            print("Existing clinets today====",disctinct_ext_today_list)
            # existing_funded_today=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday,date_today],id__in=disctinct_ext_today_list).count()
            existing_funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(trans_type=0,trans_status__gt=1,id__in=disctinct_ext_today_list).values_list('accnt_no',flat=True))
            print("Ext=====",existing_funded_today_list)
            existing_funded_clients=TblClients.objects.filter(login__in=existing_funded_today_list)
            print("List====",existing_funded_clients)
        except Exception as e:
            print("Exception---",e)
        return existing_funded_clients,date_today,date_yesterday
    #Existing funded click
    def existing_funded_click(self,fromdate,todate):
        try:
            existing_funded_today_list=""
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
                
            else:
                date_yesterday= datetime.today()-timedelta(week_day)
            
            
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            one_week=datetime.today()-timedelta(days=7)
            one_week=one_week.strftime("%Y-%m-%d")
            if fromdate=="":
                
                existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__lt=one_week).exclude(isib=1).values_list('login',flat=True))
            else:
                existing_clients_today=list(TblClients.objects.filter(livestatus="Live",converteddate__date__range=[fromdate,todate]).exclude(isib=1).values_list('login',flat=True))
           
            existing_today=TblEwalletTransaction.objects.using('svg').filter(accnt_no__in=existing_clients_today).values('accnt_no').annotate(Max('id'))
            get_ext_today_id=TblEwalletTransaction.objects.using('svg').filter(id__in=Subquery(existing_today.values('id__max')))
            
            disctinct_ext_today_list=[]
            for id in get_ext_today_id.iterator():
                disctinct_ext_today_list.append(id.id)

            print("Existing clinets today====",disctinct_ext_today_list)
            # existing_funded_today=TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),trans_date__date__range=[date_yesterday,date_today],id__in=disctinct_ext_today_list).count()
            existing_funded_today_list=list(TblEwalletTransaction.objects.using('svg').filter(Q(trans_type=0,trans_status=1)|Q(trans_type=1,trans_status=1),id__in=disctinct_ext_today_list).values_list('accnt_no',flat=True))
            print("Ext=====",existing_funded_today_list)
            existing_funded_clients=TblClients.objects.filter(login__in=existing_funded_today_list)
            print("List====",existing_funded_clients)
        except Exception as e:
            print("Exception---",e)
        return existing_funded_clients,date_today,date_yesterday


        

        

    


        

        





    

    


    
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
def dll_demo_account(user,server,password,name,email,phone,country,userpassword):
       
      
        details="NAME="+name+"^EMAIL="+email+"^PHONE="+phone+"^USER_COUNTRY"+country+"^USER_PASSWORD"+userpassword
        received="reciveddata"
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        DemoAccount_Create = hllDll.DemoAccount_Create
        hllDll.DemoAccount_Create.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.DemoAccount_Create.restype = c_int
        username=int(user)
        login = c_int(username)
        connect=DemoAccount_Create(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,c_char_p(details.encode('utf-8')).value)
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
        Cursor.execute("set nocount on;exec SP_UpdateSalesLead %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[name,email,phone,subject,ticket,country,clientarea,potential,city,address,state,zipcode,nationality,profession,dob,income,networth,experience,hear,email2,phone2,country2,noemail,title,hyplinks,appform,age,category,userId,language,training])
        updates=Cursor.fetchone()
        
     except Exception as e:
                print("Exception------",e)
     finally:
                Cursor.close()

# def get_ticket_count_for_summary(userId):
#     try:
#         Cursor=connection.cursor()
#         Cursor.execute("set nocount on;exec SP_SalesTicketCountByRepWeekly %s,%s",['D',userId])
#         counts=Cursor.fetchone()
#     except Exception as e:
#             print("Exception------",e)
#     finally:
#             Cursor.close()
#     return counts






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
            
            Cursor.execute("set nocount on;exec SP_UpdateClientDetailsSales %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[login,name,groups,country,city,zipcode,address,phone,email,comment,id,agent,ppassword,leverage,state,taxrate,tinno,enabled,sendreports,readonly,changepwd,rdcomment,terminated,termincomment,red,green,blue,color,mothername,nationality,language,created,dob,income,worth,profession,email2,phone2,country2,title,userId,ticket,subject,clientarea,potential,exp,hear,noemail,hyplink,appform,age,category,scomments])
            update_result=Cursor.fetchone()
            
            if update_result:
                update_result=update_result[0]
            
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return update_result



def open_html(body):
    
    foldername="templates\\test"
    filename = "index.html"
    if not os.path.isdir(foldername):
        os.mkdir(foldername)
    filepath = os.path.join(foldername, filename)
    # write the file
    open(filepath, "w",encoding="utf-8").write(body)
    # open in the default browser
    return filepath


        
    
    












        


