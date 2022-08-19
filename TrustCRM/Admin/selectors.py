from django.db import connection
from datetime import datetime, timedelta
from ctypes import *
import subprocess

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
    def get_leads(self,lead):
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
            if lead=="all":
                Cursor.execute("exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",["1900-01-01",date_today,'',0,0,'',0])
                leads_data=Cursor.fetchall() 
            else:
                Cursor.execute("exec SP_GetNewSalesLeadsPaginate_PY %s,%s,%s,%s,%s,%s,%s",[date_yesterday,date_today,'',0,0,'',0])
                leads_data=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return leads_data
    
    #Get Tickets
    def get_tickets(self,userId,ticket,load):
        try:
            Cursor=connection.cursor()
            print("GET Tickets--------------------- ",load)
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                    date_yesterday = datetime.today()-timedelta(3)
            else:
                date_yesterday = datetime.today()-timedelta(1)
                    
            date_yesterday=date_yesterday.strftime("%Y-%m-%d") 
            if(ticket == "pending"):
                if(load=="all"):
                    print("Load all pending")
                    Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,"1900-01-01",date_today,'P',0])
                    _tickets=Cursor.fetchall()  
                else:
                    print("Laod Pending")
                    Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,date_yesterday,date_today,'P',0])
                    _tickets=Cursor.fetchall()
            if(ticket=="resolved"):
                if(load=="all"):
                    print("Load all resolved")
                    Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,"1900-01-01",date_today,'R',0])
                    _tickets=Cursor.fetchall()
                else:
                    print()
                    Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,date_yesterday,date_today,'R',0])
                    _tickets=Cursor.fetchall()
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return _tickets  
    
    # Get New Accounts page data
    def get_new_accounts(self):
        try:
           Cursor=connection.cursor()
           date_today=datetime.today().date()    
           date_today=date_today.strftime("%Y-%m-%d")
           Cursor.execute("set nocount on;exec SP_GetNewAccountsList %s,%s,%s",["1900-01-01",date_today,'Live'])  
           live_accounts=Cursor.fetchall()
           print("Live Accounts",live_accounts)
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


    
    # Logout Procedure call

    def user_logout(self,userId):
        try:
           Cursor=connection.cursor()
           
           Cursor.execute("set nocount on;exec SP_SetUserStatus %s",[userId])           
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()

    
        


