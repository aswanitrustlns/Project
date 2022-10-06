from django.db import connection
class Services:
    def change_password(self,request):
        try:
            masterPwd=request.POST.get('masterpwd')
            investorPwd=request.POST.get('investorpwd')
            phonePwd=request.POST.get('phonepwd')
            login=request.POST.get('login')
            userId=request.session.get('userId')
            Cursor=connection.cursor()    
            Cursor.execute("exec SP_ChangePasswords %s,%s,%s,%s,%s",[masterPwd,investorPwd,phonePwd,login,userId])
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()
