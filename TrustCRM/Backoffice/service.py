import email
from email import message
from fileinput import filename
import string
from turtle import st
from django.db import connection

from TrustCRM.settings import PROJECT_ROOT, UPLOAD_ROOT
from .emailservice import EmailServices
from datetime import datetime, timedelta
from ctypes import *
from .dllservice import DllService
import os

demoserver = "50.57.14.224:443"
demopwd = "Tc2022"
demouser = "601"
dllservice=DllService(demoserver,demopwd,demouser)

emailservice=EmailServices()

class Services:
    def change_password(self,request):
        try:
            masterPwd=request.POST.get('masterpassword')
            investorPwd=request.POST.get('investorpassword')
            phonePwd=request.POST.get('phonepassword')
            login=int(request.POST.get('login'))
            userId=int(request.session.get('UserId'))
            print("Change password==========================",masterPwd,investorPwd,phonePwd,login,userId)
            
            
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_ChangePasswords %s,%s,%s,%s,%s",[masterPwd,investorPwd,phonePwd,login,userId])
            # dllservice.dll_chnage_password(masterPwd,investorPwd,phonePwd,login)
            if(Cursor.nextset()):

                print("Result========================================",Cursor.nextset())
            emailservice.password_reset_info(masterPwd,investorPwd,phonePwd,login)
            emailservice.change_password_notification(login)
            # result=Cursor.fetchone()
            # print("Result========================================",result)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
    #Update details=======
    def update_details(self,request):
        try:

            login=int(request.POST.get('formacc'))
            print("Login====",login)
            ticket=request.POST.get('ticket')
            name=request.POST.get('firstname')
            groups=request.POST.get('Group')
            
            country=int(request.POST.get('country1'))
            city=request.POST.get('city')

            zipcode=request.POST.get('zipcode')
            if zipcode!=None:
                zipcode=int(zipcode)
            else:
                zipcode=0
            print("Zip code========",zipcode)
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            email1=request.POST.get('email1')
            idno=request.POST.get('idno')
            leverage=int(request.POST.get('Leverage'))
            print("Leverage======",leverage)
            regdates=request.POST.get('regdate')
            # if regdate!=None:
            #     regdates=datetime.strptime(regdate,"%Y-%m-%d%H:%M")
            # print("Reg date======",regdates,type(regdates))
            comment=request.POST.get('comment')
            taxrate=0.0
            tinno=request.POST.get('tinno')
            enabled=request.POST.get('enabled')
            if(enabled=="on"):
                enabled=1
            else:
                enabled=0
            color=request.POST.get('color')
            if color!=None:
                color=int(color)
            else:
                color=0
            agent=request.POST.get('agent')
            if agent!=None:
                agent=int(agent)
            else:
                agent=0
            rdonly=request.POST.get('readonly')
            if(rdonly=="on"):
                rdonly=1
            else:
                rdonly=0
            sendreport=request.POST.get('sendreport')
            if(sendreport=="on"):
                sendreport=1
            else:
                sendreport=0
            changepwd=request.POST.get('changepwd')
            if(changepwd=="on"):
                changepwd=1
            else:
                changepwd=0
            ppwd=request.POST.get('ppwd')
            refcode=request.POST.get('refcode')
            source=request.POST.get('source')
            mothername=request.POST.get('mothername')
            nationality=int(request.POST.get('nationality'))
            
            created=request.POST.get('createdby')
            if created!=None:
                created=int(created)
            else:
                created=0
            dob=request.POST.get('dob')
            income=request.POST.get('income')
            if income!=None:
                income=float(income)
            else:
                income=0
            worth=request.POST.get('worth')
            if worth!=None:
                worth=float(worth)
            else:
                worth=0
            deposit=request.POST.get('deposit')
            
            if deposit!=None:
                deposit=float(deposit)
            else:
                deposit=0
            profession=request.POST.get('profession')
            risk=request.POST.get('Risk')
            riskCategory=int(request.POST.get('RiskCategory'))
            acctype=request.POST.get('Account')
            if acctype!=None:
                acctype=int(acctype)
            else:
                acctype=0
            email2=request.POST.get('email2')
            phone2=request.POST.get('phone2')
            title=request.POST.get('title')
            terminated=request.POST.get('terminated')
            if terminated=="on":
                terminated=1
            else:
                terminated=0
            state=request.POST.get('state')
            
            red=0
            blue=0
            green=0
            score=request.POST.get('score')
            if score!=None:
                score=float(score)
            else:
                score=0.0
            termComment=request.POST.get('terComment')
            rdonlycomment=request.POST.get('comment')
            country2=request.POST.get('country2')
            if country2!=None:
                country2=int(country2)
            else:
                country2=0
            user=request.session.get('UserId')
            mpwd=request.POST.get('mpwd')
            ipwd=request.POST.get('ipwd')
          
            Cursor=connection.cursor()
            Cursor.execute("exec SP_UpdateClientDetailsWithLog %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[login,ticket,name,groups,country,city,zipcode,address,phone,email1,idno,leverage,regdates,comment,taxrate,tinno,enabled,color,agent,rdonly,sendreport,changepwd,ppwd,refcode,source,mothername,nationality,created,dob,income,worth,deposit,profession,risk,riskCategory,acctype,email2,phone2,title,terminated,state,risk,red,blue,green,score,termComment,rdonlycomment,country2,user,mpwd,ipwd])
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
    #Save activity log
    def save_activity_log(self,logdata,user,type):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_SaveActivityLog %s,%s,%s",[logdata,user,type])
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
     #Update Client Area Credential
    def update_client_area(self,accno,oldemail,newemail):
        try:
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_UpdateClientAreaCredential %s,%s,%s",[oldemail,newemail,accno])
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
     #Save card
    def save_credit_card(self,request):
        try:
            accno=request.POST.get('accno')
            name=request.POST.get('holdername')
            cardno=request.POST.get('digits')
            expmonth=int(request.POST.get('expmonth'))
            expyear=int(request.POST.get('expyear'))
            cardtype=request.POST.get('cardtype')
            front=request.FILES.get('front',None)
            back=request.FILES.get('back',None)
            userid=int(request.session.get('UserId'))
            imagedata1=""
            imagedata2=""
            extension1=""
            extension2=""
            imagename=""
            contenttype=""
            contenttypebk=""
            message="Please try again"
            if front:
                

                extension1 = os.path.splitext(str(front))[1]
                imagename=os.path.splitext(str(front))[0]
                file_path="static\\uploads\\"
                # file_path=os.path.join(UPLOAD_ROOT,accno)
                print("File existance======",file_path,os.path.isfile(file_path))
                if os.path.isfile(file_path):
                    os.mkdir(file_path)
                fullpath=cardno+"front"+extension1
                fullfilepath=os.path.join(file_path,fullpath)
                with open(fullfilepath, 'wb+') as destination:
                    for chunk in front.chunks():
                        imagedata1=chunk
                        # destination.write(chunk)
            if back: 
                if imagename=="" :
                    imagename=os.path.splitext(str(back))[0]
                extension2 = os.path.splitext(str(back))[1]
                # file_path=os.path.join(UPLOAD_ROOT,accno)
                if os.path.isfile(file_path):
                    os.mkdir(file_path)
                fullpath=cardno+"back"+extension1
                fullfilepath=os.path.join(file_path,fullpath)
                with open(fullfilepath, 'wb+') as destination:
                    for chunk in back.chunks():
                        imagedata2=chunk
                        # destination.write(chunk)   
                              
            if(extension1==".doc"):
                contenttype = "application/vnd.ms-word"
            if(extension1== ".docx"):
                contenttype = "application/vnd.ms-word"
            if(extension1==".xls"):
                contenttype = "application/vnd.ms-excel"
            if(extension1==".xlsx"):
                contenttype = "application/vnd.ms-excel"
            if(extension1==".jpg"):
                contenttype = "image/jpg"
            if(extension1==".JPG"):
                contenttype = "image/jpg"
            if(extension1==".JPEG"):
                contenttype = "image/jpg"
            if(extension1==".jpeg"):
                contenttype = "image/jpg"
            if(extension1==".png"):
                contenttype = "image/png"
            if(extension1==".PNG"):
                contenttype = "image/png"
            if(extension1==".gif"):
                contenttype = "image/gif"
            if(extension1==".GIF"):
                contenttype = "image/gif"
            if(extension1==".bmp"):
                contenttype = "image/bmp"
            if(extension1==".BMP"):
                contenttype = "image/bmp"
            if(extension1== ".pdf"):
                contenttype = "application/pdf"
            if(extension1==".PDF"):
                contenttype = "application/pdf"

            if(extension2==".doc"):
                contenttypebk = "application/vnd.ms-word"
            if(extension2== ".docx"):
                contenttypebk = "application/vnd.ms-word"
            if(extension2==".xls"):
                contenttypebk = "application/vnd.ms-excel"
            if(extension2==".xlsx"):
                contenttypebk = "application/vnd.ms-excel"
            if(extension2==".jpg"):
                contenttypebk = "image/jpg"
            if(extension2==".JPG"):
                contenttypebk = "image/jpg"
            if(extension2==".JPEG"):
                contenttypebk = "image/jpg"
            if(extension2==".jpeg"):
                contenttypebk = "image/jpg"
            if(extension2==".png"):
                contenttypebk = "image/png"
            if(extension2==".PNG"):
                contenttypebk = "image/png"
        
            if(extension2==".gif"):
                contenttypebk = "image/gif"
                
            if(extension2==".GIF"):
                contenttypebk = "image/gif"
            if(extension2==".bmp"):
                contenttypebk = "image/bmp"
            if(extension2==".BMP"):
                contenttypebk = "image/bmp"
            if(extension2== ".pdf"):
                contenttypebk = "application/pdf"
            if(extension2==".PDF"):
                contenttypebk = "application/pdf"
                            
                
         
            accno=int(accno)   
            encoding = 'utf-8'
            # imagedata1.decode(encoding)
            # imagedata2.decode(encoding)
            
            print("Image data 1=====",type(imagedata1))
            print("Account data===============================",accno,name,cardno,expmonth,expyear,cardtype,userid,front,back,extension1,extension2)
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_AddNewCard %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,name,cardno,expmonth,expyear,0,imagedata1,imagedata2,imagename,contenttype,contenttypebk,cardtype,userid])
            message="Credit Card added Successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
     #Save bank account
    def save_bank_account(self,request):
        try:
            message="Please try again"
            acNo=int(request.POST.get('bankAccountno'))
            actname=request.POST.get('Bank-Accountname')
            actno=request.POST.get('Bank-Accountno')
            bankname=request.POST.get('Bankname')
            bankaddress=request.POST.get('Bankaddress')
            swiftcode=request.POST.get('Swiftcode')
            otherinfo=request.POST.get('Otherinformation')
            iban=request.POST.get('iban')
            userid=int(request.session.get('UserId'))
            flag=request.POST.get('flag')
            id=request.POST.get('id')
            print("Flag=======,id",flag,id)
            if(flag=="0"):
                flag=int(flag)
            else:
                flag=1
            if(id==""):
                id=0
            else:
                id=int(id)
            print("eeeeeeeeeeeeeeeeeeeeeeee",acNo,actname,actno,bankname,bankaddress,swiftcode,otherinfo,0,0,userid,iban)
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_SaveBankDetails %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[acNo,actname,actno,bankname,bankaddress,swiftcode,otherinfo,flag,id,userid,iban])
            message="Bank details saved successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message

    #Save credit card details
    def save_crypto_card(self,request):
        try:
            message="Please try again"
            accno=request.GET.get('accno')
            orderno=request.GET.get('orderno')
            if orderno=="":
                orderno=0
            else:
                orderno=int(orderno)
            name=request.GET.get('name')
            cardno=request.POST.get('cardno')
        
            userid=int(request.session.get('UserId'))
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_UpdateCreditCardDetails %s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,orderno,name,cardno,1,0,0,"Crypto",userid])
            message="Crypto saved successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    #save client documnets
    def save_cliet_documents(self,request):
        try:
            print("Request=======",request)
            accno=int(request.POST.get('accno'))
            expdate=request.POST.get('expdate')
            docId=request.POST.get('doctype')
            date_today=datetime.today().date()  

            uploaded_date=date_today.strftime("%Y-%m-%d")
            docfile=request.FILES.get('docfile',None)
            
            userid=int(request.session.get('UserId'))
            imagedata=""
            
            extension=""
            
            imagename=""
            contenttype=""
           
            message="Please try again"

            if docfile:

                extension = os.path.splitext(str(docfile))[1]
                imagename=os.path.splitext(str(docfile))[0]
                file_path="static\\uploads\\"
                # file_path=os.path.join(UPLOAD_ROOT,accno)
                print("File existance======",file_path,os.path.isfile(file_path))
                if os.path.isfile(file_path):
                    os.mkdir(file_path)
                fullpath=imagename
                fullfilepath=os.path.join(file_path,fullpath)
                with open(fullfilepath, 'wb+') as destination:
                    for chunk in docfile.chunks():
                        imagedata=chunk
                        # destination.write(chunk)
            
                              
            if(extension==".doc"):
                contenttype = "application/vnd.ms-word"
            if(extension== ".docx"):
                contenttype = "application/vnd.ms-word"
            if(extension==".xls"):
                contenttype = "application/vnd.ms-excel"
            if(extension==".xlsx"):
                contenttype = "application/vnd.ms-excel"
            if(extension==".jpg"):
                contenttype = "image/jpg"
            if(extension==".JPG"):
                contenttype = "image/jpg"
            if(extension==".JPEG"):
                contenttype = "image/jpg"
            if(extension==".jpeg"):
                contenttype = "image/jpg"
            if(extension==".png"):
                contenttype = "image/png"
            if(extension==".PNG"):
                contenttype = "image/png"
            if(extension==".gif"):
                contenttype = "image/gif"
            if(extension==".GIF"):
                contenttype = "image/gif"
            if(extension==".bmp"):
                contenttype = "image/bmp"
            if(extension==".BMP"):
                contenttype = "image/bmp"
            if(extension== ".pdf"):
                contenttype = "application/pdf"
            if(extension==".PDF"):
                contenttype = "application/pdf"
            
            print("Account data===============================",accno,imagedata,imagename,contenttype,"",uploaded_date,expdate,userid,docId,1)
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_SaveClientDocuments %s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,imagedata,imagename,contenttype,"",uploaded_date,expdate,userid,docId,1])
            message="Document Uploaded Successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    #Approve client documnets
    def approve_client_documents(self,accno,docs,status,reasons,userid):
        try:
            print("Request=======",accno,docs,status,reasons,userid)
            strdoclist=','.join([str(elem) for elem in docs])
            strreasons=','.join([str(elem) for elem in reasons])
            # docs=str(docs)
            print("Strrrrrr",strdoclist)
            print("Strrrrrr",strreasons)
            Cursor=connection.cursor()   
            Cursor.execute("exec SP_RejectDocumentWithEmail %s,%s,%s,%s,%s",[accno,userid,status,strreasons,strdoclist])
            print("Query execurted")
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
    #create multiple account
    def create_multiple_account(self,accno,userid):
        try:
            message=""
            Cursor=connection.cursor()   
            Cursor.execute("exec SP_CreateMultipleAccount %s,%s",[accno,userid])
            print("Query executed")
            message="Multiple accounts created successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    
    
    
   



  


