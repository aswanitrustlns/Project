from email import message
from unittest import result
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
            print("Date of birth------------------------",dob)
            print("Test-----------------------------",income,hear_bout,experience,dob,type(experience))
            if not zip_code:
                zip_code=0
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


    #Save meeting score
    def save_meeting_score(self,request):
        try:
            ticket=499015
            userId=request.session.get('UserId')
            experience=request.GET.get('experience')
            meeting=request.GET.get('meeting')
            forex=request.GET.get('forex')
            seminar=request.GET.get('seminar')
            questions=request.GET.get('questions')
            voice=request.GET.get('voice')
            trading=request.GET.get('trading')
            profession=request.GET.get('profession')
            refernce=request.GET.get('refernce')
            total=request.GET.get('total')
            Cursor=connection.cursor()
            print("experience",experience,"meeting",meeting,"forex",forex,"seminar",seminar,"questions",questions,"voice",voice,"trading",trading,"profession",profession,"ref",refernce,"total",total)
            Cursor.execute("set nocount on;exec SP_SaveMeetingScore %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[ticket,experience,meeting,forex,seminar,questions,voice,trading,profession,refernce,userId,total,'a'])
            meeting_score=Cursor.fetchone()
            # if(Cursor.nextset()):
            #     result=Cursor.fetchone()
            #     print("Result-----------------------",result)
            print("Meeting Score-----------------------------",meeting_score)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return meeting_score

    #Assign Button Click
    def assign_ticket(request):
        try:
            Cursor=connection.cursor()
            tiket=request.GET.get('ticket')
            sales_rep=request.GET.get('salesrep')
            percentage=request.GET.get('percentage')
            reassined=request.GET.get('reassined')
            userid=request.session.get('UserId')
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
    #Send meeting request
    def send_meeting_request(self,request):
        try:
            ticket=request.GET.get('ticket')
            flag=request.GET.get('flag')
            location=request.GET.get('location')
            selected_date=request.GET.get('selectedDate')
            selected_time=request.GET.get('selectedTime')
            purpose=request.GET.get('purpose')
            feedback=request.GET.get('feedback')
            userId=request.session.get('UserId')
            meeting_id=request.GET.get('meetingId')   
                  
            Cursor=connection.cursor()
           
            Cursor.execute("set nocount on;exec SP_InsertMeeting %s,%s,%s,%s,%s,%s,%s,%s,%s",[selected_date,selected_time,location,purpose,feedback,flag,userId,ticket,meeting_id])
            status=Cursor.fetchone()
            print("status after meeting request-----",status)
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()
        return status



     # Assign salesRep


    def assign_salesRep(self,request):
        try:
            userId=request.session.get('UserId')
            assign_flag='A' or 'M' or 'R'
            ticket_no=request.GET.get('ticket')
            salesrepid=request.GET.get('repid')
            percentage=request.GET.get('percentage')
            reassignid=request.GET.get('reassign')
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;SP_AssignSalesRep %s,%s,%s,%s,%s,%s",[ticket_no,salesrepid,assign_flag,percentage,reassignid,userId])
            assign_rep=Cursor.fetchone()
        except Exception as e:
            print("Exception------",e)
        finally:
            Cursor.close()

    #Update meeting feedback

    def meeting_feedback_update(self,request):
            try:
                Cursor=connection.cursor()
                ticket=request.GET.get('ticket')
                print("Ticket",type(ticket),ticket)
                location=request.GET.get('location')
                selected_date=request.GET.get('selectedDate')
                selected_time=request.GET.get('selectedTime')
                purpose=request.GET.get('purpose')
                feedback=request.GET.get('feedback')
                userId=request.session.get('UserId')            
                meeting_id=int(request.GET.get('meetingId') )
                selected_date=datetime.strptime(selected_date,'%Y-%m-%d')
                selected_time=datetime.strptime(selected_time,'%H:%M')
                print("date",type(selected_date),selected_date,"time",type(selected_time),selected_time,"userid",type(userId),"meeting id",type(meeting_id))
                latitude="0"
                longitude="0"
                
                Cursor.execute("set nocount on;exec SP_UpdateMeetingFeedback %s,%s,%s,%s,%s,%s,%s,%s,%s,%s",[ticket,selected_date,selected_time,location,purpose,feedback,latitude,longitude,meeting_id,userId])
                                 

            except Exception as e:
                print("Exception------",e)
            finally:
                Cursor.close()
            



    
        

       

