from ctypes import *
import re
#dll for change password
class DllService:
     
    def __init__(self,demoserver,demopwd,demouser) :
         self.demoserver=demoserver
         self.demopwd=demopwd
         self.demouser=demouser

    def dll_chnage_password(self,user,server,password,masterPwd,investorPwd,phonePwd,accountno):
        print("Password change dll call",user,server,password,masterPwd,investorPwd,phonePwd,accountno)
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Passwords_Change = hllDll.Passwords_Change
        hllDll.Passwords_Change.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Passwords_Change.restype = c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        connect=Passwords_Change(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no,c_char_p(masterPwd.encode('utf-8')).value,c_char_p(investorPwd.encode('utf-8')).value,c_char_p(phonePwd.encode('utf-8')).value)
        print("Change password connect value",connect)
        return connect

    #dll update client MT4
    def dll_update_user(self,user,server,password,recvdata):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Update_User = hllDll.Update_User
        hllDll.Update_User.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Update_User.restype = c_char_p
        username=int(user)
        login = c_int(username)
        
        userc=Update_User(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,c_char_p(recvdata))
        #resul=string_at(user)
        #dataset=str(resul, 'utf-8')
        return "Updated Successfully"

     #dll create client MT4
    def dll_create_user(self,user,server,password,recvdata):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll")
        Create_User = hllDll.create_new_user
        hllDll.create_new_user.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.create_new_user.restype = c_int
        username=int(user)
        login = c_int(username)
        
        userc=Create_User(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,c_char_p(recvdata))
        # print("Userc=====",userc)
        # result=string_at(userc)
        
        # dataset=str(result, 'utf-8')
        # print("Dataset====",dataset)
        #dataset=str(resul, 'utf-8')
        return userc
        

    #dll update status
    def dll_update_status(self,user,server,password,accountno,status):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        UpdateStatus = hllDll.UpdateStatus
        hllDll.UpdateStatus.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.UpdateStatus.restype = c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        print("Data=====",type(user),type(server),type(password),type(accountno),type(status),user)
        upstatus=UpdateStatus(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,c_char_p(status.encode('utf-8')))
        print("Updated  status===",upstatus)
       
        return upstatus

    #dll get currency
    def dll_get_currency(self,user,server,password,accountno):
       
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetCurrency = hllDll.GetCurrency
        hllDll.GetCurrency.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.GetCurrency.restype = c_char_p
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        currency=GetCurrency(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no)
        return currency
    def dll_get_groups(self,user,server,password):
       
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetGroups = hllDll.GetGroups_withLP
        hllDll.GetGroups_withLP.argtype = c_char_p,c_int,c_char_p
        hllDll.GetGroups_withLP.restype = POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        groups=GetGroups(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value)
        resul=string_at(groups)
        output_str=[]
        dataset=str(resul, 'utf-8')
        if(len(dataset)!=0):                
            dataset=dataset.split(",")              
            output_str=dataset
            output_str=' '.join(output_str).split()
        else:
            output_str =[]    
        return output_str
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
    def dll_enable_update(self,user,server,password,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Enable_Update = hllDll.Enable_Update
        hllDll.Enable_Update.argtype = c_char_p,c_int,c_char_p,c_int
        hllDll.Enable_Update.restype = c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        updates=Enable_Update(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        return updates
    #dll client Info
    def dll_client_info(self,user,server,password,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Get_ClientInfo = hllDll.Get_ClientInfo
        hllDll.Get_ClientInfo.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.Get_ClientInfo.restype =  POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        info=Get_ClientInfo(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        
        resul=string_at(info)
        print("Result=======",resul)
        dataset=str(resul, 'utf-8')
        print("data set======",dataset)
        details=[]
        if(len(dataset)!=0):
                
                output_str=dataset.replace("~","")
                output_str=output_str.split("^")  
                if(output_str):              
                    for i in output_str:
                        data=i.split("=")
                        details.append(data[1])
                        
        return details
    #dll get IP
    def dll_get_IP(self,user,server,password,accountno):
        mt4ip=""
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetIp = hllDll.GetIp
        hllDll.GetIp.argtype = c_char_p,c_int,c_char_p,c_char_p
        hllDll.GetIp.restype = c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        info=GetIp(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        if info:
            resul=string_at(info)
            mt4ip=str(resul, 'utf-8')
        return mt4ip
     #dll client Info time
    def dll_client_info_time(self,user,server,password,accountno,fdate,fmonth,fyear,tdate,tmonth,tyear):
        
        dataList={}
        row_details=[]
        show_data=[]
        showdetail=[]
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Get_ClientInfo_time = hllDll.Get_ClientInfo_time
        hllDll.Get_ClientInfo_time.argtype = c_char_p,c_int,c_char_p,c_int,c_int,c_int,c_int,c_int,c_int,c_int
        hllDll.Get_ClientInfo_time.restype = POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        fdate=c_int(fdate)
        fmonth=c_int(fmonth)
        fyear=c_int(fyear)
        tdate=c_int(tdate)
        tmonth=c_int(tmonth)
        tyear=c_int(tyear)
        info=Get_ClientInfo_time(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,fdate.value,fmonth.value,fyear.value,tdate.value,tmonth.value,tyear.value)
        
        resul=string_at(info)
        dataset=str(resul, 'utf-8')
        if(len(dataset)!=0):
                
                output_str=dataset.replace("\n","")
                check=output_str.find("~")
                print("check value====",check)
                if(check>0):
                    show_details=re.split(r'[~]+',output_str)
                
                    show_data=show_details[1]
                    output_str=re.split(r'[|]+',show_details[0])
                    if(output_str):              
                        for i in output_str:
                            lpdata=i.split('^')
                            m=0
                            dataList={}
                            for j in lpdata:
                                data=j.split("=")
                                
                                if(m==4):
                                    dataList['CURRENCY']=data[0]
                                    dataList['AMOUNT']=data[1]
                                else:
                                    dataList[data[0]]=data[1]                              
                                    
                                m=m+1
                        
                            row_details.append(dataList)
                else:
                    show_data=output_str
                show_detail=show_data.split("^")  
                if(show_detail):              
                        for i in show_detail:
                            data=i.split("=")
                            showdetail.append(data[1])
                            
            
        return row_details,showdetail
    #dll client Info
    def dll_client_info_without_history(self,user,server,password,accountno):
        details=[]
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Get_ClientInfo_without_history = hllDll.Get_ClientInfo_without_history
        hllDll.Get_ClientInfo_without_history.argtype= c_char_p,c_int,c_char_p,c_int
        hllDll.Get_ClientInfo_without_history.restype =POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        info=Get_ClientInfo_without_history(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        data=string_at(info)
        result=str(data, 'utf-8')
        if(len(result)!=0):
                
                output_str=result.replace("~","")
                output_str=output_str.split("^")  
                if(output_str):              
                    for i in output_str:
                        data=i.split("=")
                        details.append(data[1])
                        
        return details
    #dll yearly deposit
    def dll_get_yearly_deposit(self,user,server,password,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetYearlyDeposit = hllDll.GetYearlyDeposit
        hllDll.GetYearlyDeposit.argtype= c_char_p,c_int,c_char_p,c_int
        hllDll.GetYearlyDeposit.restype= c_double
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        info=GetYearlyDeposit(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        print("data=====",info)
        return info

    #dll yearly deposit
    def dll_net_deposit(self,user,server,password,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetNetDeposit = hllDll.GetNetDeposit
        hllDll.GetNetDeposit.argtype= c_char_p,c_int,c_char_p,c_int
        hllDll.GetNetDeposit.restype= c_double
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        info=GetNetDeposit(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        print("Info=====",info)
        return info
    #openorclosed
    def dll_openorclosed_today(self,user,server,password,accountno):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        OpenORClosedToday = hllDll.OpenORClosedToday
        hllDll.OpenORClosedToday.argtype= c_char_p,c_int,c_char_p,c_char_p
        hllDll.OpenORClosedToday.restype= c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        info=OpenORClosedToday(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value)
        return info
      #dll deposit with comment
    def dll_deposit_comment(self,user,server,password,accountno,comment,amount):
        print("Deposit====")
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Deposit_WithComment = hllDll.Deposit_WithComment
        hllDll.Deposit_WithComment.argtype= c_char_p,c_int,c_char_p,c_int,c_char_p,c_int
        hllDll.Deposit_WithComment.restype= POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(float(amount))
        info=Deposit_WithComment(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')).value,amount)
        result=string_at(info)
        
        
        return result
    #dll withdrawel with comment
    def dll_withdraw_comment(self,user,server,password,accountno,comment,amount):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        Withdrawal_WithComment = hllDll.Withdrawal_WithComment
        hllDll.Withdrawal_WithComment.argtype= c_char_p,c_int,c_char_p,c_int,c_char_p,c_int
        hllDll.Withdrawal_WithComment.restype= POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(float(amount))
        info=Withdrawal_WithComment(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')).value,amount)
        result=string_at(info)
        
        return result
  
  
     #dll phone password
    def dll_phone_pwd(self,user,server,password,accountno,phone):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        PhonePassword_Change = hllDll.PhonePassword_Change
        hllDll.PhonePassword_Change.argtype = c_char_p,c_int,c_char_p,c_int,c_char_p
        hllDll.PhonePassword_Change.restype = c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        pwdchange=PhonePassword_Change(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,c_char_p(phone.encode('utf-8')))
        return pwdchange

    #credit in with comment
    def dll_creditin_with_comment(self,user,server,password,accountno,comment,amount,expday,expmonth,expyear):
        
      
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        CreditIn_WithComment = hllDll.CreditIn_WithComment
        hllDll.CreditIn_WithComment.argtype= c_char_p,c_int,c_char_p,c_int,c_char_p,c_double,c_int,c_int,c_int
        hllDll.CreditIn_WithComment.restype = POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(float(amount))
        expday=c_int(expday)
        expmonth=c_int(expmonth)
        expyear=c_int(expyear)
        print("Inside dll")
        info=CreditIn_WithComment(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')),amount,expday.value,expmonth.value,expyear.value)
        
        result=string_at(info)
        print("Info=====",result)
        
        return result
        
      #credit out with comment
    def dll_creditout_with_comment(self,user,server,password,accountno,comment,amount):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        CreditOut_WithComment = hllDll.CreditOut_WithComment
        hllDll.CreditOut_WithComment.argtype= c_char_p,c_int,c_char_p,c_int,c_char_p,c_double
        hllDll.CreditOut_WithComment.restype = c_int
        username=int(user)
        login = c_int(username)
        account_no=c_int(accountno)
        amount=c_double(float(amount))
        
        info=CreditOut_WithComment(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no.value,c_char_p(comment.encode('utf-8')),amount)
        result=string_at(info)
        print("Result====",result)
        return result
      #dll get history
    def dll_get_history(self,user,server,password,fdate,fmonth,fyear,tdate,tmonth,tyear):
        dataList={}
        row_details=[]
        show_data=[]
        showdetail=[]
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetHistory = hllDll.GetHistory
        hllDll.GetHistory.argtype = c_char_p,c_int,c_char_p,c_int,c_int,c_int,c_int,c_int,c_int
        hllDll.GetHistory.restype = POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        
        fdate=c_int(fdate)
        fmonth=c_int(fmonth)
        fyear=c_int(fyear)
        tdate=c_int(tdate)
        tmonth=c_int(tmonth)
        tyear=c_int(tyear)
        info=GetHistory(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,fdate.value,fmonth.value,fyear.value,tdate.value,tmonth.value,tyear.value)
        resul=string_at(info)
        dataset=str(resul, 'utf-8')
        if(len(dataset)!=0):
                
                output_str=dataset.replace("\n","")
                check=output_str.find("~")
                print("check value====",check)
                if(check>0):
                    show_details=re.split(r'[~]+',output_str)
                
                    show_data=show_details[1]
                    output_str=re.split(r'[|]+',show_details[0])
                    if(output_str):              
                        for i in output_str:
                            lpdata=i.split('^')
                            m=0
                            dataList={}
                            for j in lpdata:
                                data=j.split("=")
                                
                                if(m==4):
                                    dataList['CURRENCY']=data[0]
                                    dataList['AMOUNT']=data[1]
                                else:
                                    dataList[data[0]]=data[1]                              
                                    
                                m=m+1
                        
                            row_details.append(dataList)
                else:
                    show_data=output_str
                show_detail=show_data.split("^")  
                if(show_detail):              
                        for i in show_detail:
                            data=i.split("=")
                            showdetail.append(data[1])
                            
            
                
        return row_details,showdetail
    #Inter account transfer
    def dll_inter_account_transfer(self,user,server,password,accountno1,accountno2,comment1,comment2,amount):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        InterAccount = hllDll.InterAccount
        hllDll.InterAccount.argtype= c_char_p,c_int,c_char_p,c_int,c_char_p,c_int,c_char_p
        hllDll.InterAccount.restype = POINTER(c_char_p)
        username=int(user)
        login = c_int(username)
        account_no1=c_int(accountno1)
        account_no2=c_int(accountno2)
        amount=c_double(float(amount))
        
        info=InterAccount(c_char_p(server.encode('utf-8')).value,login.value,c_char_p(password.encode('utf-8')).value,account_no1.value,c_char_p(comment1.encode('utf-8')),amount,account_no2.value,c_char_p(comment2.encode('utf-8')))
        result=string_at(info)
        return result
      #Get IBCommision report
    def dll_ib_commision_report(self,fdate,fmonth,fyear,tdate,tmonth,tyear,logins):
        
        hllDll = CDLL(r"C:\\pyenv\\TrustManagerAPI.dll") 
        GetIBCommissionReport = hllDll.GetIBCommissionReport
        hllDll.InterAccount.argtype= c_int,c_int,c_int,c_int,c_int,c_int,c_char_p
        hllDll.InterAccount.restype = c_char_p
        
        fdate=c_int(fdate)
        fmonth=c_int(fmonth)
        fyear=c_int(fyear)
        tdate=c_int(tdate)
        tmonth=c_int(tmonth)
        tyear=c_int(tyear)
        info=GetIBCommissionReport(fdate.value,fmonth.value,fyear.value,tdate.value,tmonth.value,tyear.value,c_char_p(logins.encode('utf-8')))
        result=string_at(info)
        
        dataset=str(result, 'utf-8')
        return dataset
