from django.db import connection
import string
import random
from django.template.loader import render_to_string
class Selector: 
    def generatepassword(self):
        try:
           master_pwd=random_pwd_gen()
           investor_pwd=random_pwd_gen()
           phone_pwd=random_pwd_gen()
           print("master",master_pwd,"Investor",investor_pwd,"phone",phone_pwd)
        except Exception as e:
            print("Exception----",e)
        return master_pwd,investor_pwd,phone_pwd
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
    #Load account details
    def loadAccountDetails(self,acno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetClientDetails %s",[acno]) 
            account_details=Cursor.fetchone()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return account_details
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
    #Load comment
    def loadComment(self,ticket):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetTicketLogs %s",[ticket]) 
            comments=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return comments
    #Single or multiple check
    def duplicate_account(self,accno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetDuplicateAccounts %s",[accno]) 
            duplicate=Cursor.fetchone()
            if duplicate:
                duplicate=duplicate[0]
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return duplicate
    #Client category
    def clientCategory(self,accno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetAccTypeClientCategory %s",[accno]) 
            category=Cursor.fetchone()
            if category:
                category=category[0]
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return category


    

           
   
#Random password generator
def random_pwd_gen():
        all = string.ascii_letters + string.digits
        password = "".join(random.sample(all,8))
        return password