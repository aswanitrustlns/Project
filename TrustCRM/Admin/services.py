from django.db import connection
from .selectors import Selector
from datetime import datetime, timedelta
import socket
selector=Selector()

class Services:


    def lead_registration(self,request,UserId):
        try:
            Cursor=connection.cursor()
            
            title=request.POST.get('title')
            name=request.POST.get('name')
            age=request.POST.get('age')
            email_avl=request.POST.getlist('email_agree')
            email1=request.POST.get('email1')
            email2=request.POST.get('email2')
            mobile=request.POST.get('mobile')
            telephone=request.POST.get('telephone')
            profession=request.POST.get('profession')
            subject=request.POST.get('subject')
            state=request.POST.get('state')
            address=request.POST.get('address')
            city=request.POST.get('city')
            zip_code=request.POST.get('zipcode')
            income=request.POST.get('income')
            hear_bout=request.POST.get('hearabout')
            experience=request.POST.get('experience')
            experience=int(str(experience))
            dob=request.POST.get('dob')
            print("Test-----------------------------",income,hear_bout,experience,dob,type(experience))
            if not zip_code:
                zip_code=None
            mobile_country_code=request.POST.get('mobile_country') #Get ContryID
            source=selector.get_user_name(UserId)
            
            print("Source222",source)
            
            country1=selector.get_country_code(mobile_country_code)
            if country1:
                country1=country1[0]
            telephone_country_code=request.POST.get('tel_country')#Get ContryID          
            country2=selector.get_country_code(telephone_country_code)
            if country2:
                country2=country2[0]
            
            reg_date=datetime.today().date()
            reg_date=reg_date.strftime("%m-%d-%Y")
            updated_date=datetime.now()
            
            updated_date=updated_date.strftime("%m-%d-%Y %H:%M:%S")
            
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)
            print("Updated date---------------",updated_date)
            print(country1)
            print(type(country1))
            print(country2)
            print(type(country2))
            print(type(IPAddr))
            print("print------",title,name,email_avl,email1,email2,profession,subject,source,state,address,city,zip_code,mobile,telephone,mobile_country_code,telephone_country_code,country1,country2,IPAddr)

            print("Lead submit ")        
            Cursor.execute("EXEC SP_InsertSalesLeadReg_CRM_PY %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[name,mobile,telephone,email1,email2,address,city,zip_code,source,UserId,updated_date,updated_date,title,profession,"Pending",state,country1,country2,subject,age,IPAddr,experience,hear_bout,dob,income])
            ticket=Cursor.fetchone() 
           
        except Exception as e:
                print("Exception---",e)
        finally:
            Cursor.close()
        return ticket

    def create_ticket_service(self,request):
        try:
            Cursor=connection.cursor()
            demoid=request.GET.get('id')
            UserId=request.session.get('UserId')
            print("demo iddd nd user id-----",demoid,UserId)
            ticket_data=selector.create_new_ticket(demoid)
            print("Demo id-----",ticket_data[0],type(ticket_data[0]))

            print("Ticket data after ----------",ticket_data)
            email=ticket_data[2]
            phone=ticket_data[4]
            print("Inserted data----",ticket_data[1],ticket_data[4],ticket_data[2],ticket_data[3],ticket_data[5],ticket_data[6],ticket_data[7],ticket_data[13],ticket_data[10],ticket_data[15],ticket_data[16],ticket_data[18],ticket_data[11],ticket_data[22],UserId,ticket_data[1])
            Cursor.execute("EXEC SP_CreateTicket %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[ticket_data[1],ticket_data[4],ticket_data[2],ticket_data[3],ticket_data[5],ticket_data[6],ticket_data[7],ticket_data[13],ticket_data[10],ticket_data[15],ticket_data[16],ticket_data[18],ticket_data[11],ticket_data[22],UserId,ticket_data[0]])
           
            print("Ticket created successfully-----")
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return email,phone

