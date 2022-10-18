from email import message
from sqlite3 import Cursor
from django.db import connection
import string
import random
from django.template.loader import render_to_string
import binascii
from datetime import datetime

from TrustCRM.settings import UPLOAD_ROOT
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
            duplicate=Cursor.fetchall()
            if duplicate:
                duplicate=duplicate[0]
            print("Duplicate========",duplicate)
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
            msg="Account approved successfully"
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return msg
     #approve client
    def approveClient(self,accno,userId):
        try:
            msg="Account approved in MT4. Database update failed"
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_ApproveClient %s,%s",[accno,userId]) 
            
            msg="Account approved successfully"
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return msg

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
            message="Account terminated successfully"
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return message
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
            Cursor.execute("set nocount on;exec SP_GetComplianceDetails %s,%s",[complaintId,"nodata"]) 
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
            commision=Cursor.fetchone()
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return commision
    #Load  creditcard details
    def load_credit_card_details(self,accno):
        try:
            details=""
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetCreditCardDetails %s",[accno])
            details=Cursor.fetchall()
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return details
     #Load  crypto details
    def load_crypto_card_details(self,accno):
        try:
            details=""
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetCryptoCardDetails %s",[accno])
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
            bankdetails=""
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

    #view side image
    def get_card_front(self,id,accno,side):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetCreditCardClicked %s,%s,%s",[accno,id,side])
            image_detail=Cursor.fetchone()
            image_path=""
            if image_detail:
                
                imagedata=image_detail[0]
                imagetype=image_detail[1]
                imagename=image_detail[2]
                image_path=create_image(imagedata,imagetype,imagename)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return image_path
     #view document image
    def get_documnet_image(self,id,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetDocumentClicked %s,%s",[accno,id])
            image_detail=Cursor.fetchone()
            
            image_path=""
            if image_detail:
                
                imagedata=image_detail[0]
                imagetype=image_detail[1]
                imagename=image_detail[2]
                image_path=create_image(imagedata,imagetype,imagename)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return image_path
    #Get client documents
    def get_client_documents(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetClientDocuments %s",[accno])
            doc_details=Cursor.fetchall()
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return doc_details
    #Get activity details
    def get_client_activites(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_GetDocumentsLog %s",[accno])
            doc_log=Cursor.fetchall()
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return doc_log
    #Check mandatory documents
    def check_mandatory_documents(self,accno):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on;exec SP_CheckMandatoryDocs %s",[accno])
            result=Cursor.fetchone()
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return result
    #Get reject reasons Using reason id 
    def get_reason(self,reasons):
        try:
            reasonStr=[]
            for reason in reasons:
                print("Reasons=====",reason)
                Cursor=connection.cursor()    
                Cursor.execute("set nocount on;select Rejected_Reason from tbl_RejectReason_Master where id=%s",[reason])
                result=Cursor.fetchone()
                reasonStr.append(result[0])
            print("Result=====",reasonStr)    
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return reasonStr  
    #MT4 password checking
    def mt4_password_checking(self,username,server,password):
        try:
          connect=dllservice.dll_connection(username,server,password)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return connect
     #Phone password reset
    def phone_password_reset(self,accno):
        try:
            newPwd=random_pwd_gen()
            print("New password====",newPwd)
            Cursor=connection.cursor()    
            Cursor.execute("set nocount on; exec SP_ChangePhonePasswords %s,%s",[newPwd,accno])
            # connect=dllservice.dll_phone_pwd(accno,newPwd)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close
        return newPwd

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
            print("activity Logs")
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return activity_logs

    #Insert ticket logs procedure
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
    
   
  
  
#create image
def create_image(imagedata,imagetype,imagename):
   
    contenttype=imagetype
    if(imagetype=="application/vnd.ms-word"):
            contenttype = ".doc"
    if(imagetype=="application/vnd.ms-word"):
        contenttype = ".docx"
    if(imagetype=="application/vnd.ms-excel"):
        contenttype = ".xls"
    if(imagetype=="application/vnd.ms-excel"):
        contenttype = ".xlsx"
    if(imagetype=="image/jpg"):
        contenttype =".jpg" 
    if(imagetype=="image/jpg"):
        contenttype = ".JPG"
    if(imagetype=="image/jpg"):
        contenttype = ".JPEG"
    if(imagetype=="image/jpg"):
        contenttype = ".jpeg"
    if(imagetype=="image/png"):
        contenttype = ".png"
    if(imagetype=="image/png"):
        contenttype =".PNG" 
        
    if(imagetype=="image/gif"):
        contenttype =".gif" 
                
    if(imagetype=="image/gif"):
        contenttype =".GIF" 
    if(imagetype=="image/bmp"):
        contenttype = ".bmp"
    if(imagetype=="image/bmp"):
        contenttype = ".BMP"
    if(imagetype== "application/pdf"):
        contenttype = ".pdf"
    if(imagetype=="application/pdf"):
        contenttype = ".PDF"
    print("Content type====",contenttype)
    
    imagename=imagename+contenttype
    
    file_path="static\\uploads"+"\\"+imagename
    print("Image name=====",imagename)
    # with open('binary_file') as file: 
    #     data = file.read() 
    res = ''.join(format(x, '02x') for x in imagedata)
    result=str(res)
    data = bytes.fromhex(result) 
    with open(file_path, 'wb') as file: 
        file.write(data)
    return file_path

        




    

           
   
#Random password generator
def random_pwd_gen():
        all = string.ascii_letters + string.digits
        password = "".join(random.sample(all,8))
        return password