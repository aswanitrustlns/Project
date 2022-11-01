from typing import List
from django.db import connection
from datetime import datetime, timedelta
from .emailservices import EmailServices
emailservice=EmailServices()
class Services:
#Get seminar

    def get_last_seminar(self):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_GetSeminars")
            last_seminar=Cursor.fetchall()
            last_tuples = list((sem[0]) for sem in last_seminar)
            reverse_seminar=list(reversed(last_tuples))
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return reverse_seminar
    
# #Get Seminars

#     def get_seminars(self):
#         try:
#             Cursor=connection.cursor()
#             seminar_list=Cursor.execute("set nocount on;exec SP_GetSeminars")
#         except Exception as e:
#                 print("Exception---",e)
#         finally:
#             Cursor.close()
#         return seminar_list
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
            title=""
            if titleen=="None":
                title=titlear
            if titlear=="None":
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
            regdatear=request.POST.get('ardate')

            reg_time=request.POST.get('time')
            reg_timear=request.POST.get('artime')
            print("=================================",aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,regdatear,regdate,reg_time,reg_timear)
            if regdate==None and reg_time==None:
                if reg_timear:
                    reg=regdatear+" "+reg_timear
                else:
                    reg=regdatear
            if regdate!=None and reg_time!=None:
                if reg_time:
                    reg=regdate+" "+reg_time
                else:
                    reg=regdate
            print("Date time==========",reg)
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
            regdatear=request.POST.get('ardate')

            reg_time=request.POST.get('time')
            reg_timear=request.POST.get('artime')
            print("=================================",aname,alocation,elvl,webp,description,ardesc,subdes,arsubdes,regdatear,regdate,reg_time,reg_timear)
            print("Bullettt======",bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5)
            if regdate==None and reg_time==None:
                if reg_timear:
                    reg=regdatear+""+reg_timear
                else:
                    reg=regdatear
            if regdate!=None and reg_time!=None:
                if reg_time:
                    reg=regdate+""+reg_time
                else:
                    reg=regdate
            regDate=datetime.strptime(reg,"%Y-%m-%d%H:%M")
            print("Date time==========",regDate,type(regDate))
            Cursor.execute("set nocount on;exec SP_UpdateEventDetails %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[title,name,location,aname,alocation,regDate,elvl,webp,description,ardesc,subdes,arsubdes,bullet1,bullet2,bullet3,bullet4,bullet5,abullet1,abullet2,abullet3,abullet4,abullet5])
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
            # seminarList = sorted(seminarList, key=lambda k: k['id'], reverse=True)
            # print("Seminars..................",seminarList)  
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
            print("SEmianr id=====",seminar)
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

#Load sales rep

    def get_salesrep_permission(self,userId):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetSalesRepPermission  %s",[userId]) 
            permission=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return permission
        
#Load Country

    def loadCountry(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetSalesLeadCountry") 
            all_country=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return all_country
#Source List Ticket
    def load_source_list(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetSourceListTicket") 
            source_list=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return source_list

#Load nationality
    def load_nationality(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetNationality") 
            nationality=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return nationality

#Load language
    def load_language(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_GetLanguageList") 
            language_list=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return language_list
    
#Load Confirmation grid
    def load_confirmation_grid(self,request):
        try:
            Cursor=connection.cursor()           
            userid=request.session.get('UserId')
            fromdate=request.GET.get('from')
            todate=request.GET.get('to')
            load_data=[]
            # status=request.POST.get('source')
            status="P"
            repId=request.GET.get('repId')
            if repId:
                repId=int(repId)
            country=request.GET.get('country')
            if country:
                country=int(country)
            search=request.GET.get('search')
            source=request.GET.get('source')
            if source=="0":
                source=""
        
            nationality=request.GET.get('nationality')
            if nationality:
                nationality=int(nationality)
            # pageno=request.POST.get('pageno')
            pageno=0
            # pagecount=0
            # pagecount=request.POST.get('pagecount')
            lbflag=request.GET.get('lbflag')
           
            Cursor.execute("set nocount on;exec SP_GetSalesLeadsListCount_PY %s,%s,%s,%s,%s",[userid,fromdate,todate,status,repId])
            pagecount=Cursor.fetchone()
            if pagecount:
                pagecount=int(pagecount[0])
            print("PageCount=================================",pagecount)
            print("Data===========================================",userid,fromdate,todate,status,repId,country,search,source,nationality,pageno,pagecount,lbflag)
            if pagecount>0:
                Cursor.execute("set nocount on;exec SP_GetSalesLeadsListPaginate %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[userid,fromdate,todate,status,repId,country,search,source,nationality,pageno,pagecount,lbflag]) 
                load_data=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return load_data
        
 #Get Upcoming seminar
    def get_upcoming_seminar(self):
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_UpcomingSeminars") 
            seminarlist_upcoming=Cursor.fetchall()
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return seminarlist_upcoming
   # Register Seminar
    def register_seminar(self,title,name,to_addr,seminartitle,ticket,userid):
        register_msg=""
        try:
            Cursor=connection.cursor()           
            Cursor.execute("set nocount on;exec SP_SeminarConfirmation %s,%s,%s",[ticket,userid,seminartitle]) 
            register_msg=Cursor.fetchone()
            print("Register mesage================",register_msg)
            
            if register_msg:
                if(register_msg[0]=='Seminar Confirmed Successfully'):
                   emailservice.seminar_confirmation_email(title,name,to_addr,seminartitle)
        except Exception as e:
                print("Exception------",e)
        finally:
                Cursor.close()
        return register_msg
    #Email template send---

    def email_template_selection(self,lang,subject,fromaddr,to,title,name,userId,ticket,salesrep):
        try:
            Cursor=connection.cursor()
            emailservice.send_email_templates(lang,subject,to,title,name,salesrep)
            print("Selector----",lang,subject,fromaddr,to,title,name)
            history="Send --xxxxxx[Eng]-- SMS for Ticket xxx"
            chattype=""
            dept=""
            Cursor.execute("set nocount on;exec SP_UpdateChatAndLog %s,%s,%s,%s,%s",[userId,history,chattype,ticket,dept])
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
    def upcoming_seminar_details(self,seminarId):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_UpcomingSeminarByTitle %s",[seminarId])
            details=Cursor.fetchone()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return details

        


        


       


