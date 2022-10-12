import email
from django.db import connection
from .emailservice import EmailServices
from datetime import datetime, timedelta
from ctypes import *
from .dllservice import DllService

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
            login=int(request.POST.get('accno'))
            ticket=request.POST.get('ticket')
            name=request.POST.get('firstname')
            groups=request.POST.get('Group')
            
            country=int(request.POST.get('country1'))
            city=request.POST.get('city')

            zipcode=int(request.POST.get('zipcode'))
            print("Zip code========",zipcode)
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            email1=request.POST.get('email1')
            idno=request.POST.get('idno')
            leverage=int(request.POST.get('Leverage'))
            print("Leverage======",leverage)
            regdate=request.POST.get('regdate')
            comment=request.POST.get('comment')
            taxrate=0.0
            tinno=request.POST.get('tinno')
            enabled=request.POST.get('enabled')
            if(enabled=="on"):
                enabled=1
            else:
                enabled=0
            color=request.POST.get('color')
            if color:
                color=int(color)
            agent=request.POST.get('agent')
            if agent:
                agent=int(agent)
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
            if created:
                created=int(created)
            else:
                created=0
            dob=request.POST.get('dob')
            income=request.POST.get('income')
            if income:
                income=float(income)
            worth=request.POST.get('worth')
            if worth:
                worth=float(worth)
            deposit=request.POST.get('deposit')
            
            if deposit:
                deposit=float(deposit)
            profession=request.POST.get('profession')
            risk=request.POST.get('Risk')
            riskCategory=int(request.POST.get('RiskCategory'))
            acctype=request.POST.get('Account')
            if acctype:
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
            if score:
                score=float(score)
            else:
                score=0.0
            termComment=request.POST.get('terComment')
            rdonlycomment=request.POST.get('comment')
            country2=request.POST.get('country2')
            if country2:
                country2=int(country2)
            else:
                country2=0
            user=request.session.get('UserId')
            mpwd=request.POST.get('mpwd')
            ipwd=request.POST.get('ipwd')
            print("Data=======1",)
            print("Data2=====",)
            print("Date3=========",)
            Cursor=connection.cursor()
            Cursor.execute("exec SP_UpdateClientDetailsWithLog %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[login,ticket,name,groups,country,city,zipcode,address,phone,email1,idno,leverage,regdate,comment,taxrate,tinno,enabled,color,agent,rdonly,sendreport,changepwd,ppwd,refcode,source,mothername,nationality,created,dob,income,worth,deposit,profession,risk,riskCategory,acctype,email2,phone2,title,terminated,state,risk,red,blue,green,score,termComment,rdonlycomment,country2,user,mpwd,ipwd])
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
     #Save card
    def save_credit_card(self,request):
        try:
            accno=request.POST.get('accno')
            name=request.POST.get('holdername')
            cardno=request.POST.get('digits')
            expmonth=request.POST.get('expmonth')
            expyear=request.POST.get('expyear')
            cardtype=request.POST.get('cardtype')
            front=request.FILES['front']
            back=request.FILES['back']
            userid=request.session.get('UserId')
            print("Account data===============================",accno,name,cardno,expmonth,expyear,cardtype,front,back,userid)
            # Cursor=connection.cursor()    
            # Cursor.execute("exec SP_SaveActivityLog %s,%s,%s",[logdata,user,type])
        except Exception as e:
            print("Exception----",e)
        finally:
            pass
            # Cursor.close()

  


