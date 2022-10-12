from sqlite3 import Cursor
from django.db import connection
import string
import random
from django.template.loader import render_to_string
from .dllservice import DllService
demoserver = "50.57.14.224:443"
demopwd = "Tc2022"
demouser = "601"
dllservice=DllService(demoserver,demopwd,demouser)

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

    #temperory approve client
    def tmpApproveClient(self,accno,userId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_TmpApproveClient %s,%s",[accno,userId]) 
            # category=Cursor.fetchone()
            
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
    
     #approve client
    def approveClient(self,accno,userId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_ApproveClient %s,%s",[accno,userId]) 
            # category=Cursor.fetchone()
            
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()

    #Get email details
    def get_email_details(self,accno):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetEmailDetails %s",[accno]) 
            account_details=Cursor.fetchone()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return account_details
    

    #Reject documnet
    def rejectdocument(self,accno,reasonId,description,status,user):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_RejectDocument %s,%s,%s,%s,%s",[accno,reasonId,description,status,user]) 
            
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
    
    #Update account status
    def update_account_status(self,livestatus,accno,clientarealogin,userId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_UpdateAccountStatusReadOnly %s,%s,%s,%s",[livestatus,accno,clientarealogin,userId]) 
            result=Cursor.fetchone()
            print("rsult======",result)
            if result:
                result=result[0]
            
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return result
    #Get reject date
    def get_reject_date(self,accno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetRejectedDate %s",[accno]) 
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
    #Get documents verified poi
    def get_docs_verified_poi(self,accno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_CheckDocsVerifiedPOI %s",[accno]) 
            result=Cursor.fetchone()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return result
     #Get documents verified
    def get_docs_verified(self,accno):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_CheckDocsVerified %s",[accno]) 
            result=Cursor.fetchone()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return result
    #Get complaince details
    def get_complains_details(self,complaintId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetComplianceDetails %s",[complaintId]) 
            result=Cursor.fetchone()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return result
    #change phone password
    def change_phone_pwd(self,accno,phonepwd):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_ChangePhonePasswords %s,%s",[accno,phonepwd]) 
            # category=Cursor.fetchone()
            
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
    #Account update form
    def account_update_form(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_AccountUpdateForm %s",[accno])
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
    #Load commision structure
    def load_commision_structure(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_LoadCommissionStructure %s",[accno])
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
    #Load  creditcard details
    def load_credit_card_details(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetCreditCardDetails %s",[accno])
            details=Cursor.fetchall()
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return details
    #Load card info
    def get_user_details(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetAcctBasicDts %s",[accno])
            details=Cursor.fetchall()
            
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return details

    #varify credit card
    def verify_redit_card_details(self,id,accno,status,userid):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_VerifyCreditCard %s,%s,%s,%s",[id,accno,status,userid])
            
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
    #credit card count
    def get_credit_card_count(self,accno):
        
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetCreditCardCount %s",[accno])
            count=Cursor.fetchone()    
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return count
     #credit card count
    def get_bank_details(self,accno):
        
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetBankDetails %s",[accno])
            bankdetails=Cursor.fetchall()    
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return bankdetails
    #verify bank details
    def verify_bank_details(self,id,accno,status,userid):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_VerifyBankDetails %s,%s,%s,%s",[id,accno,status,userid])
            
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        
        




    

           
   
#Random password generator
def random_pwd_gen():
        all = string.ascii_letters + string.digits
        password = "".join(random.sample(all,8))
        return password