import email
from email import message
from fileinput import filename
import string
from turtle import st
from django.db import connection

from decimal import Decimal    
from .emailservice import EmailServices
from datetime import datetime, timedelta
from ctypes import *
from .dllservice import DllService
import os
from .selector import Selector
demoserver = "50.57.14.224:443"
demopwd = "trust123"
demouser = "505"
dllservice=DllService(demoserver,demopwd,demouser)
selector=Selector()
emailservice=EmailServices()

class Services:
    def change_password(self,request):
        try:
            masterPwd=request.POST.get('masterpassword')
            investorPwd=request.POST.get('investorpassword')
            phonePwd=request.POST.get('phonepassword')
            login=int(request.POST.get('login'))
            userId=int(request.session.get('UserId'))
            user=request.session.get('user')
            server=request.session.get('server')
            password=request.session.get('password')
            print("Change password==========================",masterPwd,investorPwd,phonePwd,login,userId)
            
            
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_ChangePasswords %s,%s,%s,%s,%s",[masterPwd,investorPwd,phonePwd,login,userId])
            dllservice.dll_chnage_password(user,server,password,masterPwd,investorPwd,phonePwd,login)
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
            if(address==None):
                address=""
            phone=request.POST.get('phone')
            if(phone==None):
                phone=""
            email1=request.POST.get('email1')
            idno=request.POST.get('idno')
            leverage=int(request.POST.get('Leverage'))
            print("Leverage======",leverage)
            regdates=request.POST.get('regdate')
            print("reg dates======",regdates,type(regdates))
            if regdates!="":
                regdates=datetime.strptime(regdates,"%Y-%m-%d")
            print("Reg date======",regdates,type(regdates))
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
            user=request.session.get('user')
            server=request.session.get('server')
            password=request.session.get('password')
            Cursor=connection.cursor()
            print("data",login,ticket,name,groups,country,city,zipcode,address,phone,email1,idno,leverage,regdates,comment,taxrate,tinno,enabled,color,agent,rdonly,sendreport,changepwd,ppwd,refcode,source,mothername,nationality,created,dob,income,worth,deposit,profession,risk,riskCategory,acctype,email2,phone2,title,terminated,state,red,blue,green,score,termComment,rdonlycomment,country2,user,mpwd,ipwd)
            Cursor.execute("exec SP_UpdateClientDetailsWithLog %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[login,ticket,name,groups,country,city,zipcode,address,phone,email1,idno,leverage,regdates,comment,taxrate,tinno,enabled,color,agent,rdonly,sendreport,changepwd,ppwd,refcode,source,mothername,nationality,created,dob,income,worth,deposit,profession,risk,riskCategory,acctype,email2,phone2,title,terminated,state,red,blue,green,score,termComment,rdonlycomment,country2,user,mpwd,ipwd])
            message="Updated Successfully"
            
            update_data="NAME="+name+"^GROUP="+groups+"^CITY="+city+"^ZIPCODE="+str(zipcode)+"^ADDRESS="+address+"^PHONE="+phone+"^EMAIL="+email1+"^COMMENT"+comment+"^USERID="+user+"^USER_AGENT="+str(agent)+"^USER_LEVERAGE="+str(leverage)+"^USER_STATE="+state+"^USER_TAXES="+str(taxrate)+"^USER_COUNTRY="+str(country)+"^LOGIN_NO="+str(login)+"^USER_ENABLE="+str(enabled)+"^USER_ENABLE_READONLY="+str(rdonly)+"^USER_ENABLE_CHANGE_PASSWORD="+str(changepwd)+"^USER_SEND_REPORTS="+str(sendreport)+"^USER_COLOR_NONE="+str(color)+"^RED="+str(red)+"^GREEN="+str(green)+"^BLUE="+str(blue)+"^GROUPCHANGE="+str(groups)
            update_data=bytes(update_data.encode())
            result=dllservice.dll_update_user(user,server,password,update_data)
            print("Result===",result)
            info=dllservice.dll_client_info(user,server,password,login)
            print("data=====",info)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
            return message
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
            cardId=request.POST.get('cardId')
            print("Card Id======",cardId)
            front=request.FILES.get('front',None)
            print("Front=====",front)
            back=request.FILES.get('back',None)
            userid=int(request.session.get('UserId'))
            imagedata1=None
            imagedata2=None
            extension1=None
            extension2=None
            imagename=""
            contenttype=""
            contenttypebk=""
            message="Please try again"
            message="Please upload Card "
            file_path="static\\uploads\\"
            print("File path===")
            if front!=None:
                
                
                extension1 = os.path.splitext(str(front))[1]
                imagename=os.path.splitext(str(front))[0]
                fullname=imagename+extension1
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
            print("Front image")
            if back!=None: 
                if imagename=="" :
                    imagename=back #os.path.splitext(str(back))[0]
                extension2 = os.path.splitext(str(back))[1]
                fullname=imagename+extension2
                # file_path=os.path.join(UPLOAD_ROOT,accno)
                if os.path.isfile(file_path):
                    os.mkdir(file_path)
                fullpath=cardno+"back"+extension2
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
            
            # imagedata1.decode(encoding)
            # imagedata2.decode(encoding)
            
            print("Image data 1=====",type(imagedata1))
            print("Account data===============================",accno,name,cardno,expmonth,expyear,cardtype,userid,front,back,extension1,extension2)
            Cursor=connection.cursor()    
            if front!=None or back!=None:
                Cursor.execute("exec SP_AddNewCard %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,name,cardno,expmonth,expyear,0,imagedata1,imagedata2,fullname,contenttype,contenttypebk,cardtype,userid])
            else:
                print("Without image=====",accno,cardId,name,cardno,1,expmonth,expyear,cardtype,userid)
                Cursor.execute("exec SP_UpdateCreditCardDetails %s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,cardId,name,cardno,1,expmonth,expyear,cardtype,userid])
            message="Card added Successfully"
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
            flag=int(request.POST.get('flag'))
            id=request.POST.get('id')
            print("Flag=======",flag,id)
            
            if(id==""):
                id=0
            else:
                id=int(id)
            print("eeeeeeeeeeeeeeeeeeeeeeee",flag)
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
            accno=request.POST.get('accno')
            orderno=request.POST.get('orderno')
            if orderno=="":
                orderno=0
            else:
                orderno=int(orderno)
            name=request.POST.get('holdername')
            cardno=request.POST.get('wallet')
        
            userid=int(request.session.get('UserId'))
            Cursor=connection.cursor()    
            print("Save crypto card=====",accno,orderno,name,cardno,userid)
            Cursor.execute("exec SP_UpdateCreditCardDetails %s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,orderno,name,cardno,1,0,0,"Crypto",userid])
            message="Crypto card saved successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    #save client documnets
    def save_cliet_documents(self,request):
        try:
            
            accno=int(request.POST.get('accno'))
            expdate=request.POST.get('expdate')
            docId=request.POST.get('doctype')
            
            Id=request.POST.get('id')
            print("Id=====",Id)
            if(Id=="" or Id==None):
                Id=0
            else:
                Id=int(Id)
            date_today=datetime.today().date() 
            description="" 
            if(docId=="25"):
                description="Account Update Form"
            if(docId=="10"):
                description="Articles of Association"
            if(docId=="11"):
                description="Bank Statement"
            if(docId=="12"):
                description="Business Plan"
            if(docId=="15"):
                description="Certificate Of Formation"
            if(docId=="17"):
                description="Closed Account"
            if(docId=="20"):
                description="CRS Report"
            if(docId=="2"):
                description="ID/Passport Copy"
            if(docId=="5"):
                description="Individual Account Opening"
            if(docId=="13"):
                description="Login Confirmation"
            if(docId=="14"):
                description="Memorandum"
            if(docId=="18"):
                description="Miscellaneous"
            if(docId=="21"):
                description="Professional Client Form"
            if(docId=="3"):
                description="Proof of Address"
            if(docId=="23"):
                description="Risk Assessment Form"
            if(docId=="6"):
                description="Signature"
            if(docId=="16"):
                description="Termination Letter"
            if(docId=="24"):
                description="Trading Statements"
            if(docId=="19"):
                description="World Compliance Check"
            if(docId=="22"):
                description="Other"


            uploaded_date=date_today.strftime("%Y-%m-%d")
            docfile=request.FILES.get('docfile',None)
            
            userid=int(request.session.get('UserId'))
            imagedata=""
            
            extension=""
            
            imagename=""
            contenttype=""
            fullname=""
           
            message="Please try again"
            Cursor=connection.cursor()  
            if docfile:

                extension = os.path.splitext(str(docfile))[1]
                imagename=os.path.splitext(str(docfile))[0]
                fullname=imagename+extension
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
                
                print("Account data===============================",accno,fullname,contenttype,description,uploaded_date,expdate,userid,docId,Id)
                
                Cursor.execute("exec SP_SaveClientDocuments %s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,imagedata,fullname,contenttype,description,uploaded_date,expdate,userid,docId,Id])
                message="Document Uploaded Successfully"
            else:
               print("Data======",accno,Id,expdate,userid)
               Cursor.execute("exec SP_AddExpiryDate %s,%s,%s,%s",[accno,Id,expdate,userid]) 
               message="Updated Successfully"
            
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    #Add Expiry
    def add_expiry_documents(self,request):
        try:
            
            accno=int(request.POST.get('accno'))
            Cursor=connection.cursor() 
            expdate=request.POST.get('expdateed')
            #docId=request.POST.get('doctype')
            
            Id=request.POST.get('id')
            print("Id=====",Id)
            if(Id=="" or Id==None):
                Id=0
            else:
                Id=int(Id)                      
            userid=int(request.session.get('UserId'))          
           
            message="Please try again"
             
            print("Data======",accno,Id,expdate,userid)
            Cursor.execute("exec SP_AddExpiryDate %s,%s,%s,%s",[accno,Id,expdate,userid]) 
            message="Updated Successfully"
            
        except Exception as e:
            print("Exception----",e)
            message=str(e)+str(accno)
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
            multiple=""
            Cursor=connection.cursor()   
            Cursor.execute("set nocount on;exec SP_CreateMultipleAccount %s,%s",[accno,userid])
            multiple=Cursor.fetchone()
            if multiple:
                multiple=multiple[0]
            print("Query executed",multiple)
            message="Multiple accounts created successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return multiple

    #Save transaction
    def save_transactions(self,request):

        try:
            message="fail"
            accno=int(request.POST.get('accno'))
            fullname=request.POST.get('fullname')
            balance=float(request.POST.get('balance'))
            avl_margin=float(request.POST.get('avlmargin'))
            creditin=request.POST.get('creditin')
            status=request.POST.get('status')
            if creditin=="" or creditin==None:
                creditin=0.0
            creditout=request.POST.get('creditout')
            if creditin=="" or creditout==None:
                creditout=0.0
            deposit=request.POST.get('deposit')
            if deposit=="" or deposit==None:
                deposit=0.0
            withdrawal=request.POST.get('withdrawel')
            if withdrawal=="" or withdrawal==None:
                withdrawal=0.0
            credit=request.POST.get('credit')
            if credit=="" or credit==None:
                credit=0.0
            expdate=request.POST.get('expdate')
            comment=request.POST.get('comment')
            # initial=int(request.POST.get('initial'))
            # repId=int(request.POST.get('repId'))
            initial=0
            repId=0
            creditIndll=0
            creditOutdll=0
            user=int(request.session.get('user'))
            server=request.session.get('server')
            password=request.session.get('password')
            Cursor=connection.cursor()   
            userdetails=selector.get_user_details(accno)
            if userdetails:
                userdetails=userdetails[0]
                title=userdetails[2]
                name=userdetails[1]
                email=userdetails[0]
                currency=userdetails[5] 
            
            
            if status=="creditin":
                expdateformat=datetime.strptime(expdate,"%Y-%m-%d")
            
                expday=int(expdateformat.day)
                expmonth=int(expdateformat.month)
                expyear=int(expdateformat.year)
                acno=int(accno)
                deposit=float(deposit)
                print("Dll data=====",user,server,password,acno,comment,deposit,expday,expmonth,expyear)
                creditIndll=dllservice.dll_creditin_with_comment(user,server,password,acno,comment,deposit,expday,expmonth,expyear)
                if(creditIndll !=""):
                    Cursor.execute("exec SP_SaveTransaction %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,fullname,balance,avl_margin,creditin,creditout,deposit,withdrawal,credit,expdate,comment,initial,repId])
                    
                    editable=dllservice.dll_enable_update(user,server,password,acno)
                    print("Editable=====",editable)
                    if(editable!=0 and editable==accno):
                        selector.get_live_status(accno,0)
                    emailservice.SendCreditInConfirmation(title,name,email,accno,currency,deposit)
                    message="Credit In completed successfully"

            if status=="creditout":
                print("Credit out=======")
                message="success"
                acno=int(accno)
                deposit=float(deposit)
                creditOutdll=dllservice.dll_creditout_with_comment(user,server,password,acno,comment,deposit)
                if(creditOutdll!=""):
                    Cursor.execute("exec SP_SaveTransaction %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,fullname,balance,avl_margin,creditin,creditout,deposit,withdrawal,credit,expdate,comment,initial,repId])
                    emailservice.SendCreditOutConfirmation(title,name,email,accno,currency,deposit)
                    message="Credit Out completed successfully"
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    #Update ewallet transaction
    def update_ewallet_transactions(self,request):

        try:
            message=""
            accno=request.POST.get('accno')
            
            walletstatus=request.POST.get('status')
            print("walletstatus===",walletstatus)
            fullname=request.POST.get('fullname')
            credit=request.POST.get('credit')
            amount=request.POST.get('amount')
            
            balance=float(request.POST.get('balance'))
            avl_margin=float(request.POST.get('avlmargin'))
            print("wallet depo",balance,avl_margin)
            # withdrawal=float(request.POST.get('withdrawal'))
            user=int(request.session.get('user'))
            server=request.session.get('server')
            password=request.session.get('password')
            repId=request.POST.get('repId')
            initial=request.POST.get('initial')
            print("Initial======",initial)
            if(repId!=None):
                repId=int(repId)
            else:
                repId=0                    
            transId=int(request.POST.get('transactiontype'))
            print("Transaction Id===",transId)
            # status=int(request.POST.get('status'))
            status=0
            dlldepo=0
            dllwithdraw=0
            nextyr=0
            yearlydep=0
            totaldep=0
            remarks=request.POST.get('comment')
            userdetails=selector.get_user_details(accno)
            if userdetails:
                userdetails=userdetails[0]
                title=userdetails[2]
                name=userdetails[1]
                email=userdetails[0]
                currency=userdetails[5] 
            Cursor=connection.cursor()    
            if(walletstatus=="deposit"):
                acno=int(accno)
                amount=float(amount)
                message="Deposit failed in MT4"
                dlldepo=dllservice.dll_deposit_comment(user,server,password,acno,remarks,amount)
                message="Deposited successfully in MT4"
                if(dlldepo!=""):
                    withdrawal=0.0
                    print("Query execution=====")
                    message="Deposit failed in database"
                    Cursor.execute("exec SP_SaveTransaction %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,fullname,balance,avl_margin,0.0,0.0,amount,withdrawal,credit,"",remarks,0,repId])
                    emailservice.SendDepositConfirmation(title,name,email,accno,currency,amount)
                    Cursor.execute("exec SP_UpdateEWalletTransaction %s,%s,%s,%s,%s,%s,%s",[accno,amount,withdrawal,repId,transId,status,remarks])  
                    message="Deposited successfully"                  
                    editable=dllservice.dll_enable_update(user,server,password,acno)
                    print("Editable=====",editable)
                    if(editable!=0 and editable==accno):
                        if(initial=="on"):
                            selector.get_live_status(accno,amount)
                        else:
                            selector.get_live_status(accno,0)
                nextyr=selector.get_nextdepart_yearly(accno)
                
                yearlydep=dllservice.dll_get_yearly_deposit(user,server,password,acno)
                
                totaldep=dllservice.dll_net_deposit(user,server,password,acno)
                
                if(totaldep>100000):
                    profilestatus=selector.get_profile_status(accno)
                    
                    if(profilestatus=="Pending"):
                        emailservice.SendComplaince(title,name,email,accno,currency,amount,0,7)
                dormant=selector.dormant_check(accno)
                
                if(dormant==accno):
                    emailservice.SendComplaince(title,name,email,accno,currency,amount,0,4)
            print("Wallet status===",walletstatus)
            if(walletstatus=="withdraw"):
                acno=int(accno)
                trades=0
                withdrawal=amount
                print("Withdraw",withdrawal)
                message="Withdrawal Failed"
                dllwithdraw=dllservice.dll_withdraw_comment(user,server,password,acno,remarks,withdrawal)
                if(dllwithdraw!=""):
                    Cursor.execute("exec SP_SaveTransaction %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[accno,fullname,balance,avl_margin,0.0,0.0,0,withdrawal,credit,"",remarks,0,repId])
                    emailservice.SendWithdrawalConfirmation(title,name,email,accno,currency,amount)
                    Cursor.execute("exec SP_UpdateEWalletTransaction %s,%s,%s,%s,%s,%s,%s",[accno,0,withdrawal,repId,transId,status,remarks])
                    message="Withdrawal completed successfully"                    
                    trades=selector.get_trades_count(accno)
                    print("Trades======",trades)
                    if(trades!=None):
                        if(trades>=0):
                            active=-1
                            active=dllservice.dll_openorclosed_today(user,server,password,accno)
                            print("Active======",active)
                            if(trades+active < 3):
                                print("More than 3 trades=====")
                                emailservice.SendComplaince(title,name,email,accno,currency,0,5)
                else:
                    message="Withdrawal failed in MT4"
                    Cursor.execute("exec SP_UpdateEWalletTransaction %s,%s,%s,%s,%s,%s,%s",[accno,0,withdrawal,repId,transId,status,remarks])

            


        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
        return message
    #save inter account trasfer
    def interaccount_transfer(self,request):
        try:
            msg="Deposit failed in Database"
            name=request.GET.get('name')
            balance=request.GET.get('balance')
            margin=request.GET.get('margin')
            credit=0
            account1=request.GET.get('account1')
            account2=request.GET.get('account2')
            amount=request.GET.get('amount')
            initial=request.GET.get('initial')
            comment1="Withdrawal to"+account2
            comment2="Deposit from"+account1
            user=int(request.session.get('user'))
            server=request.session.get('server')
            password=request.session.get('password')
            print("Initial====",initial)
            Cursor=connection.cursor()   
            creditin=0
            creditout=0
            withdrawal=0
            expdate=""
            initial=0
            repId=0
            transfer=""
            account1=int(account1)
            account2=int(account2)
            msg="Deposit failed in MT4"
            transfer=dllservice.dll_inter_account_transfer(user,server,password,account1,account2,comment1,comment2,float(amount))
            if(transfer!=""):
                Cursor.execute("exec SP_SaveTransaction %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[account2,name,balance,margin,creditin,creditout,amount,withdrawal,credit,expdate,comment2,initial,repId])
                
            enabled=dllservice.dll_enable_update(user,server,password,account2)
            print("Enabled======",enabled)
            if(enabled!=0 and enabled==account2):
                if(initial==1):
                    selector.get_live_status(account2,amount)
                else:
                    selector.get_live_status(account1,0)
            trades=selector.get_trades_count(account1)
            print("Trades======",trades)
            if(trades!=None):
               if(trades>=0):
                    active=-1
                    active=dllservice.dll_openorclosed_today(user,server,password,account1)
                    print("Active======",active)
                    if(trades+active < 3):
                        print("More than 3 trades=====")
                        emailservice.SendComplaince(title,name,email,account1,currency,0,5)
            msg="Deposit Completed Successfully"
            userdetails=selector.get_user_details(account1)
            if userdetails:
                userdetails=userdetails[0]
                title=userdetails[2]
                name=userdetails[1]
                email=userdetails[0]
                currency=userdetails[5]
                emailservice.SendInteraccountTransferConfirmation(title,name,email,account2,account1,currency,amount)
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
            return msg