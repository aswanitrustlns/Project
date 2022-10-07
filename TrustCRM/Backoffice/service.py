from django.db import connection
from .emailservice import EmailServices
from datetime import datetime, timedelta
from ctypes import *
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
            #dll_chnage_password(masterPwd,investorPwd,phonePwd,login)
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

#dll for change password
def dll_chnage_password(masterPwd,investorPwd,phonePwd,accountno):
    demoserver = "50.57.14.224:443"
    demopwd = "Tc2022"
    demouser = "601" 
    hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
    Passwords_Change = hllDll.Passwords_Change
    hllDll.Passwords_Change = c_char_p,c_int,c_char_p,c_char_p
    hllDll.Passwords_Change.restype = c_int
    username=int(demouser)
    login = c_int(username)
    account_no=c_int(accountno)
    connect=Passwords_Change(c_char_p(demoserver.encode('utf-8')).value,login.value,c_char_p(demopwd.encode('utf-8')).value,account_no,c_char_p(masterPwd.encode('utf-8')).value,c_char_p(investorPwd.encode('utf-8')).value,c_char_p(phonePwd.encode('utf-8')).value)
    return connect
