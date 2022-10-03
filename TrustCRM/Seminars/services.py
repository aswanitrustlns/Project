from django.db import connection
from datetime import datetime, timedelta
class Services:
#Get Last seminar

    def get_last_seminar(self):
        try:
            Cursor=connection.cursor()
            last_seminar=Cursor.execute("set nocount on;exec SP_GetLastSeminar")
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return last_seminar
    
#Get Seminars

    def get_seminars(self):
        try:
            Cursor=connection.cursor()
            seminar_list=Cursor.execute("set nocount on;exec SP_GetSeminars")
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_list

#Get seminar Info list

    def get_seminar_info_list(self):
        try:
            Cursor=connection.cursor()
            seminar_info_list=Cursor.execute("set nocount on;exec SP_GetSeminarInfolist")
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_info_list

#Save new event details

    def save_new_event_details(self,request):
        try:
            Cursor=connection.cursor()
            title=request.POST.get('title')
            name=request.POST.get('name')
            location=request.POST.get('location')
            aname=request.POST.get('aname')
            alocation=request.POST.get('alocation')
            elvl=request.POST.get('elvl')
            webp=request.POST.get('webp')
            description=request.POST.get('description')
            ardesc=request.POST.get('ardesc')
            subdes=request.POST.get('subdes')
            arsubdes=request.POST.get('arsubdes')
            bullet1=request.POST.get('bullet1')
            bullet2=request.POST.get('bullet2')
            bullet3=request.POST.get('bullet3')
            bullet4=request.POST.get('bullet4')
            bullet5=request.POST.get('bullet5')
            abullet1=request.POST.get('abullet1')
            abullet2=request.POST.get('abullet2')
            abullet3=request.POST.get('abullet3')
            abullet4=request.POST.get('abullet4')
            abullet5=request.POST.get('abullet5')
            regdate=request.POST.get('regdate')
            Cursor.execute("set nocount on;exec SP_SaveNewEventDetails %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[title,name,location,aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5,regdate])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
#Update event details

    def update_event_details(self,request):
        try:
            Cursor=connection.cursor()
            title=request.POST.get('title')
            name=request.POST.get('name')
            location=request.POST.get('location')
            aname=request.POST.get('aname')
            alocation=request.POST.get('alocation')
            elvl=request.POST.get('elvl')
            webp=request.POST.get('webp')
            description=request.POST.get('description')
            ardesc=request.POST.get('ardesc')
            subdes=request.POST.get('subdes')
            arsubdes=request.POST.get('arsubdes')
            bullet1=request.POST.get('bullet1')
            bullet2=request.POST.get('bullet2')
            bullet3=request.POST.get('bullet3')
            bullet4=request.POST.get('bullet4')
            bullet5=request.POST.get('bullet5')
            abullet1=request.POST.get('abullet1')
            abullet2=request.POST.get('abullet2')
            abullet3=request.POST.get('abullet3')
            abullet4=request.POST.get('abullet4')
            abullet5=request.POST.get('abullet5')
            regdate=request.POST.get('regdate')
            Cursor.execute("set nocount on;exec SP_UpdateEventDetails %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[title,name,location,aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5,regdate])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()

#Delete seminar

    def delete_seminar(self,seminar_name):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_DeleteSeminar %s",[seminar_name])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
#Expert dropdown

    def get_expert_dropdown(self,eventid):
        try:
            Cursor=connection.cursor()
            dropdown_data=Cursor.execute("set nocount on;exec SP_GetSeminarInfoo %s",[eventid])
        except Exception as e:
                print("Exception---",e)
        finally:
             Cursor.close()
        return dropdown_data

#View webinar

    def view_webinar(self,userId):
        try:
            Cursor=connection.cursor()
            webinar_info=Cursor.execute("set nocount on;exec SP_GetSeminarInfo %s",[userId])
        except Exception as e:
                print("Exception---",e)
        finally:
             Cursor.close()
        return webinar_info


#Get Seminar Details

    def get_seminar_details(self):
        try:
            Cursor=connection.cursor()
            seminar_details_list=Cursor.execute("set nocount on;exec SP_GetSeminarDetails")
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_details_list

#Load seminars to grid

    def load_seminar_grid(self,seminar):
        try:
            Cursor=connection.cursor()
            grid_list=Cursor.execute("set nocount on;exec SP_GetSeminarsGrid %s",[seminar])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return grid_list

#Get Seminar Details

    def get_seminar_report(self,seminar):
        try:
            Cursor=connection.cursor()
            seminar_report=Cursor.execute("set nocount on;exec SP_GetSeminarsReport %s",[seminar])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_report

#Get Accounts Opened

    def get_accounts_opened(self):
        try:
            Cursor=connection.cursor()
            date_today=datetime.today().date()    
            date_today=date_today.strftime("%Y-%m-%d")
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            if(week_day==0):
                date_yesterday = datetime.today()-timedelta(3)
            else:
                date_yesterday = datetime.today()-timedelta(1)

            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            seminar_accounts=Cursor.execute("set nocount on;exec SP_SeminarAccounts %s,%s",[date_yesterday,date_today])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_accounts

#Update attending status

    def update_attending_status(self,ticket,status,seminar,userid):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_UpdateAttending %s,%s,%s,%s",[ticket,status,seminar,userid])
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
       

       


