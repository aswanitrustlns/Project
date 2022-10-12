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
        hllDll.Passwords_Change = c_char_p,c_int,c_char_p,c_char_p
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
        hllDll.Update_User = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Update_User.restype = c_char_p
        username=int(self.demouser)
        login = c_int(username)
        
        user=Update_User(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,c_char_p(recvdata))
        return user

    #dll update status
    def dll_update_status(self,recvdata,accountno,status):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        UpdateStatus = hllDll.UpdateStatus
        hllDll.UpdateStatus = c_char_p,c_int,c_char_p,c_char_p
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
        hllDll.GetCurrency = c_char_p,c_int,c_char_p,c_char_p
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
        hllDll.Enable_Update = c_char_p,c_int,c_char_p,c_char_p
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
        hllDll.Get_ClientInfo = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Get_ClientInfo.restype = c_int
        username=int(self.demouser)
        login = c_int(username)
        account_no=c_int(accountno)
        info=Get_ClientInfo(c_char_p(self.demoserver.encode('utf-8')).value,login.value,c_char_p(self.demopwd.encode('utf-8')).value,account_no.value)
        return info
    
