from django.db import connection
from datetime import datetime, timedelta

class Services:
#Get seminar

    def get_last_seminar(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSeminars")
            last_seminar=Cursor.fetchall()
            print("Last seminar=====",last_seminar)
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
#Get Last Seminars

    def get_seminars_last(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetLastSeminar")
            seminar_last=Cursor.fetchone()
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_last

#Get seminar Info list

    def get_seminar_info_list(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSeminarInfolist")
            seminar_info_list=Cursor.fetchall()
            
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_info_list

#Save new event details

    def save_new_event_details(self,request):
        try:
            Cursor=connection.cursor()
            titleen=request.POST.get('titleen')
            titlear=request.POST.get('titlear')
            if titleen:
                title=titleen
            if titlear:
                title=titlear
            name=request.POST.get('seminarname')
            location=request.POST.get('location')
            aname=request.POST.get('aname')
            alocation=request.POST.get('alocation')
            elvlen=request.POST.get('elvlen')
            elvlar=request.POST.get('elvlar')
            if elvlen:
                elvl=elvlen
            if elvlar:
                elvl=elvlar
            webpen=request.POST.get('webpen')
            webpar=request.POST.get('webpar')
            webp=0
            if webpen!=None:
                if webpen=="on":
                    webp=1
                else:
                    webp=0
            if webpar!=None:
                if webpen=="on":
                    webp=1
                else:
                    webp=0
            
            description=request.POST.get('description')
            ardesc=request.POST.get('ardesc')
            subdes=request.POST.get('subdescription')
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
            regdate=request.POST.get('date')
            reg_time=request.POST.get('time')
            reg=regdate+" "+reg_time
            print("======================",title,name,location,aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5,regdate)
            Cursor.execute("set nocount on;exec SP_SaveNewEventDetails %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[title,name,location,aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5,reg])
            print("saved")
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
#Update event details

    def update_event_details(self,request):
        try:
            Cursor=connection.cursor()
            titleen=request.POST.get('titleen')
            titlear=request.POST.get('titlear')
            if titleen:
                title=titleen
            if titlear:
                title=titlear
            name=request.POST.get('seminarname')
            location=request.POST.get('location')
            aname=request.POST.get('aname')
            alocation=request.POST.get('alocation')
            elvlen=request.POST.get('elvlen')
            elvlar=request.POST.get('elvlar')
            if elvlen:
                elvl=elvlen
            if elvlar:
                elvl=elvlar
            webpen=request.POST.get('webpen')
            print("webpen========================",webpen)
            
  
            if webpen=="on":
                    webp=1
            else:
                    webp=0
       
                
            
            description=request.POST.get('description')
            ardesc=request.POST.get('ardesc')
            subdes=request.POST.get('subdescription')
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
            regdate=request.POST.get('date')
            reg_time=request.POST.get('time')
            reg=regdate+" "+reg_time
            Cursor.execute("set nocount on;exec SP_UpdateEventDetails %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[title,name,location,aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5,reg])
            print("saved")
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

    def view_webinar(self,seminarId):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSeminarInfo %s",[seminarId])
            webinar_info=Cursor.fetchone()
        except Exception as e:
                print("Exception---",e)
        finally:
             Cursor.close()
        return webinar_info


#Get Seminar Details

    def get_seminar_details(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSeminarDetails")
            seminar_details_list=Cursor.fetchall()
            seminarList=[]
            for items in seminar_details_list:
                item=items[0]
                
                ids=item.split('/')
                ids=ids[0]
                seminarList.append({
                    "id":ids,
                    "name":items[0]
                })
            seminarList = sorted(seminarList, key=lambda k: k['id'], reverse=True)
            print("Seminars..................",seminarList)  
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminarList

#Load seminars to grid

    def load_seminar_grid(self,seminar):
        try:
            Cursor=connection.cursor()

            Cursor.execute("set nocount on;exec SP_GetSeminarsGrid %s",[seminar])
            grid_list=Cursor.fetchall()
            # print("Grid list================================",grid_list)
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return grid_list

#Get Seminar Details

    def get_seminar_report(self,seminar):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSeminarsReport %s",[seminar])
            seminar_report=Cursor.fetchall()
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_report

#Get Accounts Opened

    def get_accounts_opened(self,fromdate,todate):
        try:
            Cursor=connection.cursor()
            # date_today=datetime.today().date()    
            # date_today=date_today.strftime("%Y-%m-%d")
            # week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            # if(week_day==0):
            #     date_yesterday = datetime.today()-timedelta(3)
            # else:
            #     date_yesterday = datetime.today()-timedelta(1)

            # date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            Cursor.execute("set nocount on;exec SP_SeminarAccounts %s,%s",[fromdate,todate])
            seminar_accounts=Cursor.fetchall()
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
#Get seminar count

    def get_seminar_count(self,seminarId):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec GetSemCount %s",[seminarId])
            seminar_count=Cursor.fetchone()
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return seminar_count


       


