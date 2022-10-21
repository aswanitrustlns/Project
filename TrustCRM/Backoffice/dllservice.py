from ctypes import *
#dll for change password
class DllService:
     
    def __init__(self,demoserver,demopwd,demouser) :
         self.demoserver=demoserver
         self.demopwd=demopwd
         self.demouser=demouser

    def dll_chnage_password(self,masterPwd,investorPwd,phonePwd,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Passwords_Change = hllDll.Passwords_Change
        hllDll.Passwords_Change.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Passwords_Change.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        connect=Passwords_Change(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no,c_char_p(masterPwd.encode('utf-8')).value,c_char_p(investorPwd.encode('utf-8')).value,c_char_p(phonePwd.encode('utf-8')).value)
        return connect

    #dll update client MT4
    def dll_update_user(self,recvdata):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Update_User = hllDll.Update_User
        hllDll.Update_User.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Update_User.restype = c_char_p
        username=int(self.demouser)
        login = c_int(username)
        
        user=Update_User(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,c_char_p(recvdata))
        return user

    #dll update status
    def dll_update_status(self,recvdata,accountno,status):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        UpdateStatus = hllDll.UpdateStatus
        hllDll.UpdateStatus.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.UpdateStatus.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        status=UpdateStatus(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value,c_char_p(status))
        return status

    #dll get currency
    def dll_get_currency(self,accountno):
       
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetCurrency = hllDll.GetCurrency
        hllDll.GetCurrency.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.GetCurrency.restype = c_char_p
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        currency=GetCurrency(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no)
        return currency
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
    #dll enable update
    def dll_enable_update(self,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Enable_Update = hllDll.Enable_Update
        hllDll.Enable_Update.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Enable_Update.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        updates=Enable_Update(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return updates
    #dll client Info
    def dll_client_info(self,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Get_ClientInfo = hllDll.Get_ClientInfo
        hllDll.Get_ClientInfo.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Get_ClientInfo.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        info=Get_ClientInfo(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return info
     #dll client Info time
    def dll_client_info_time(self,accountno,fdate,fmonth,fyear,tdate,tmonth,tyear):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Get_ClientInfo_time = hllDll.Get_ClientInfo_time
        hllDll.Get_ClientInfo_time.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Get_ClientInfo_time.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        fdate=c_int(fdate)
        fmonth=c_int(fmonth)
        fyear=c_int(fyear)
        tdate=c_int(tdate)
        tmonth=c_int(tmonth)
        tyear=c_int(tyear)
        info=Get_ClientInfo_time(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value,fdate.value,fmonth.value,fyear.value,tdate.value,tmonth.value,tyear.value)
        return info
    #dll client Info
    def dll_client_info_without_history(self,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Get_ClientInfo_without_history = hllDll.Get_ClientInfo_without_history
        hllDll.Get_ClientInfo_without_history.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.Get_ClientInfo_without_history.restype = POINTER(c_char_p)
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        info=Get_ClientInfo_without_history(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return info
    #dll yearly deposit
    def dll_get_yearly_deposit(self,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetYearlyDeposit = hllDll.GetYearlyDeposit
        hllDll.GetYearlyDeposit.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.GetYearlyDeposit.restype= c_double
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        info=GetYearlyDeposit(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return info

    #dll yearly deposit
    def dll_net_deposit(self,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetNetDeposit = hllDll.GetNetDeposit
        hllDll.GetNetDeposit.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.GetNetDeposit.restype= c_double
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        info=GetNetDeposit(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return info
    #openorclosed
    def dll_openorclosed_today(self,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        OpenORClosedToday = hllDll.OpenORClosedToday
        hllDll.OpenORClosedToday.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.OpenORClosedToday.restype= c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        info=OpenORClosedToday(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return info
    #dll withdrawel with comment
    def dll_withdraw_comment(self,accountno,comment,amount):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Withdrawal_WithComment = hllDll.Withdrawal_WithComment
        hllDll.Withdrawal_WithComment.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.Withdrawal_WithComment.restype= c_double
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(amount)
        info=Withdrawal_WithComment(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')).value,amount.value)
        return info
  
  
     #dll phone password
    def dll_phone_pwd(self,accountno,phone):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        PhonePassword_Change = hllDll.changePhonePassword
        hllDll.changePhonePassword.argtype = c_char_p,c_int,c_char_p,c_int,c_char_p
        hllDll.changePhonePassword.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        pwdchange=PhonePassword_Change(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value,c_char_p(phone.encode('utf-8')))
        return pwdchange

    #credit in with comment
    def dll_creditin_with_comment(self,accountno,comment,amount,expday,expmonth,expyear):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        CreditIn_WithComment = hllDll.CreditIn_WithComment
        hllDll.CreditIn_WithComment.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.CreditIn_WithComment.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(amount)
        expday=c_int(expday)
        expmonth=c_int(expmonth)
        expyear=c_int(expyear)
        info=CreditIn_WithComment(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')),amount.value,expday.value,expmonth.value,expyear.value)
        return info
      #credit out with comment
    def dll_creditout_with_comment(self,accountno,comment,amount):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        CreditOut_WithComment = hllDll.CreditOut_WithComment
        hllDll.CreditOut_WithComment.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.CreditOut_WithComment.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(amount)
        
        info=CreditOut_WithComment(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')),amount.value)
        return info
    
