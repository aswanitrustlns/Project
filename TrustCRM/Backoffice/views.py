from atexit import register
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .service import Services
from .selector import Selector
from .emailservice import EmailServices
from .models import TblActionreasons
from datetime import datetime, timedelta

selector=Selector()
service=Services()
emailservice=EmailServices()

# Create your views here.
#change password

def change_password(request):
    if 'UserId' in request.session:
        
        return render(request,'backoffice/changepassword.html')
    else:
        return redirect('/login')
def generate_passwords(request):
    if 'UserId' in request.session:
       master_pwd,investor_pwd,phone_pwd=selector.generatepassword()
       return JsonResponse({"master":master_pwd,"investor":investor_pwd,"phone":phone_pwd})
    else:
        return redirect('/login')
def change_password_request(request):
    if 'UserId' in request.session:
        service.change_password(request)
        return JsonResponse({"success":"done"})
    else:
        return redirect('/login')
#Manage Account page
def manage_account(request):
    if 'UserId' in request.session:
        nationality=selector.load_nationality()
        country=selector.get_all_country()
        leverage=selector.loadLeverage()
        accountType=selector.loadAccountType()
        risk=selector.loadRiskCategory()
        return render(request,'backoffice/backofficemanagement.html',{"nations":nationality,'country_list':country,'leverage':leverage,'account':accountType,'risks':risk}) 
    else:
        return redirect('/login')

#Load account details
def load_account_details(request):
    if 'UserId' in request.session:
        acc_no=request.GET.get('account')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        details,otherdetails,ip=selector.loadAccountDetails(user,server,password,acc_no)
        ebalance=selector.loadEwalletBalance(acc_no)
        return JsonResponse({"detail":details,"other":otherdetails,"ip":ip,"ebalance":ebalance}) 
    else:
        return redirect('/login')
#Load account details
def load_bankaccount_details(request):
    if 'UserId' in request.session:
        acc_no=request.GET.get('account')
        details=selector.get_bank_details(acc_no)
        return JsonResponse({"details":details}) 
    else:
        return redirect('/login')
#Duplicate check
def check_duplicate(request):
    if 'UserId' in request.session:
        acc_no=request.GET.get('account')
        duplicate=selector.duplicate_account(acc_no)
        return JsonResponse({"duplicate":duplicate}) 
    else:
        return redirect('/login')
#Update Back office
def backoffice_update(request):
    if 'UserId' in request.session:
        msg=""
        acc_no=request.POST.get('formacc')
        leverage=int(request.POST.get("Leverage"))
        category=selector.duplicate_account(acc_no)
        if(category=="RC" and leverage>30):
            msg="Retail clients cannot have leverage greater than 30"
        else:
            msg=service.update_details(request)
        return JsonResponse({"msg":msg}) 
    else:
        return redirect('/login')
#Bank approval
def bank_approval(request):
    if 'UserId' in request.session:
        return render(request,"backoffice/bankapproval.html")
    else:
        return redirect('/login')

#load credit card data
def load_card_data(request):

    if 'UserId' in request.session:
        details=""
        name=""
        accno=request.GET.get('account')
        details=selector.load_credit_card_details(accno)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            name=userdetails[1]
        
        return JsonResponse({"details":details,"name":name}) 
    else:
        return redirect('/login')
#load crypto card data
def load_crypto_data(request):
    if 'UserId' in request.session:
        accno=request.GET.get('account')
        details=""
        name=""
        details=selector.load_crypto_card_details(accno)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            name=userdetails[1]
        
        return JsonResponse({"details":details,"name":name}) 
    else:
        return redirect('/login')
#Approve Card
def approve_card(request):
    if 'UserId' in request.session:
        status=request.GET.get('status')
        id=request.GET.get('id')
        userid=request.session.get('UserId')
        accno=request.GET.get('accno')
        card=request.GET.get('card')
        cardtype=request.GET.get('type')
        details=selector.verify_redit_card_details(id,accno,status,userid)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            title=userdetails[2]
            name=userdetails[1]
            email=userdetails[0]
            emailservice.SendCardApprovalmail(title,name,email,card,cardtype,status)
        return JsonResponse({"details":details}) 
    else:
        return redirect('/login')
#Approve Bank
def approve_bank(request):
    if 'UserId' in request.session:
        details=""
        status=request.GET.get('status')
        id=request.GET.get('id')
        userid=request.session.get('UserId')
        accno=request.GET.get('accno')
        card=request.GET.get('card')
        details=selector.verify_bank_details(id,accno,status,userid)
        return JsonResponse({"details":details}) 
    else:
        return redirect('/login')
#Card Save
def save_card(request):
    if 'UserId' in request.session:
        message=""
        accno=request.POST.get('accno')
        count=selector.get_credit_card_count(accno)
        if count:
            count=count[0]
            if(count>5):
                message="Cannot upload more than five Credit Cards"
            else:
                message=service.save_credit_card(request)
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')

#Save Bank account
def save_bank_account(request):
    if 'UserId' in request.session:
        message=""
        message=service.save_bank_account(request)
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Save Bank account
def save_crypto_account(request):
    if 'UserId' in request.session:
        message=""
        message=service.save_crypto_card(request)
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#View Card Front
def load_card_front(request):
    if 'UserId' in request.session:
        message=""
        id=request.GET.get('orderno')
        accno=request.GET.get('accno')
        side=request.GET.get('side')
        image_path=selector.get_card_front(id,accno,side)
        return JsonResponse({"imagepath":image_path}) 
    else:
        return redirect('/login')
#View and upload page
def view_document(request):
    if 'UserId' in request.session:
        accno=request.GET.get('accno')
        
        docs=selector.get_client_documents(accno)
        logs=selector.get_client_activites(accno)
        return render(request,"backoffice/viewandupload.html",{"docs":docs,'logs':logs})
    else:
        return redirect('/login')
#View documnet image
def load_document_image(request):
    if 'UserId' in request.session:
        message=""
        id=request.GET.get('orderno')
        accno=request.GET.get('accno')
        
        print("view card front",id,accno)
        image_path=selector.get_documnet_image(id,accno)
        return JsonResponse({"imagepath":image_path}) 
    else:
        return redirect('/login')
#Upload document
def upload_document(request):
    if 'UserId' in request.session:
        message=service.save_cliet_documents(request)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')
#Update log
def update_log(request):
    if 'UserId' in request.session:
        accno=request.GET.get('accno')
        logs=selector.get_client_activites(accno)
        return JsonResponse({"logs":logs})
    else:
        return redirect('/login')
#Get Ticket Summary
def summary_ticket(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        summary=selector.get_ticket_summary(ticket)
        print("Ticket summaryy",summary)
        return JsonResponse({"summary":summary})
    else:
        return redirect('/login')
#Get Ticket Summary
def journal_update(request):
    if 'UserId' in request.session:
        ticket=request.GET.get('ticket')
        activity=selector.get_activities_log(ticket)
        return JsonResponse({"activity":activity})
    else:
        return redirect('/login')
#Load Reminders
def load_reminders(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        ticket=request.GET.get('ticket')
        reminders=selector.load_ticket_reminders(userid,ticket)
        return JsonResponse({"reminders":reminders})
    else:
        return redirect('/login')
#Approve document
def approve_document(request):
    if 'UserId' in request.session:
        msg="Please try again"
        
        accno=int(request.GET.get('accno'))
        # docs=selector.get_client_documents(accno)
        docs=request.GET.getlist('docsId[]')
        reasons=request.GET.getlist('reasons[]')
        status=request.GET.get('status')
        print("Docs========",docs,reasons,status)
        # docslist=[x[6] for x in docs]
        # print("Docslist=====",docslist)
        userid=int(request.session.get('UserId'))
        duplicate_accounts=selector.duplicate_account(accno)
        print("Duplicate accounts=======",duplicate_accounts,type(duplicate_accounts))
        service.approve_client_documents(accno,docs,status,reasons,userid)
        if status=="A":
            doc_check=selector.check_mandatory_documents(accno)
            if doc_check:
                if doc_check[0]=="SUCCESS":
                    msg="Documents approved successfully"
                else:
                    msg="Please upload the mandatory documents, Passport Copy(With expiry date)/Proof Of Address/Indivual Account Opening Form to continue"
        else:
            print("type of reason=====",type(reasons))
            userdetails=selector.get_user_details(accno)
            if userdetails:
                userdetails=userdetails[0]
                title=userdetails[2]
                name=userdetails[1]
                email=userdetails[0]
            reason=selector.get_reason(reasons)
            emailservice.rejectLiveaccountDocs(title,name,email,reason)
            msg="Document rejected successfully"
        return JsonResponse({"message":msg})
    else:
        return redirect('/login')
 #Document expiry alert
def send_expiry_alert(request):
   if 'UserId' in request.session:
    msg=""
    accno=int(request.GET.get('accountno'))
    alert=request.GET.get('alert')
    userdetails=selector.get_user_details(accno)
    if userdetails:
        userdetails=userdetails[0]
        title=userdetails[2]
        name=userdetails[1]
        email=userdetails[0]
        emailservice.sendBDocExpiry(title,name,email,alert)
        msg="email send"
    return JsonResponse({"message":msg})
   else:
        return redirect('/login')
#MT4 Password checking
def check_mt4_password(request):
   if 'UserId' in request.session:
    message="fail"
    connect=""
    user=request.session.get('user')
    server=request.session.get('server')
    password=request.session.get('password')
    connect=selector.mt4_password_checking(user,server,password)
    if connect==0:
        message="success"
    return JsonResponse({"message":message})
   else:
        return redirect('/login')
#create multple account
def multiple_account_create(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=request.session.get('UserId')
        accno=request.GET.get('account')
        print("data   account=======",userid,accno)
        multiple=service.create_multiple_account(accno,userid)
        print("Multiple====",multiple)
        return JsonResponse({"multiple":multiple}) 
    else:
        return redirect('/login')

#commision structure load
def load_commision_structure(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=request.session.get('UserId')
        accno=request.GET.get('account')
        print("data   account=======",userid,accno)
        commision=selector.load_commision_structure(accno)
        return JsonResponse({"data":commision}) 
    else:
        return redirect('/login')
#Reset Phone Password
def reset_phone_pwd(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=int(request.session.get('UserId'))
        accno=request.GET.get('account')
        newpwd=request.GET.get('newpwd')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        print("data   account=======",userid,accno,newpwd)
        message=selector.phone_password_reset(user,server,password,accno,newpwd)
        
        userdetails=selector.get_user_details(accno)
        service.save_activity_log("Phone password reset",userid,"Phone PWD Reset")
        if userdetails:
            userdetails=userdetails[0]
            title=userdetails[2]
            name=userdetails[1]
            email=userdetails[0]
            emailservice.sendResetPWD(title,name,email,newpwd)
        message="Password changed successfully"
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Update Client area
def update_client_area_credential(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=int(request.session.get('UserId'))
        accno=request.GET.get('account')
        oldemail=request.GET.get('old')
        newemail=request.GET.get('new')
        print("data   account=======",userid,accno,oldemail,newemail)
        
        service.update_client_area(accno,oldemail,newemail)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            title=userdetails[2]
            name=userdetails[1]
            email=userdetails[0]
            emailservice.ClientAreaCredentialUpdate(title,name,email,accno)
            emailservice.ClientAreaCredentialUpdateNotify(accno)
        message="Updated successfully"
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Final approval
def final_approval(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=int(request.session.get('UserId'))
        accno=request.GET.get('account')
        ticket=request.GET.get('ticket')
        status=selector.get_docs_verified(accno)
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        docverified=1
        PORstatus=""
        if status:
            docverified=status[0]
            PORstatus=status[3]
        if docverified==0 or PORstatus=="Not Verified":
            message="POI and POR are mandatory before complete approval"
        else:
           message=selector.approveClient(user,server,password,accno,userid)
           today=datetime.today()
           one_week=datetime.today()+timedelta(days=7)
           saveReason=TblActionreasons(ticket=ticket,login=accno,action="",duedate=one_week,reason="",userid=userid,status="",updated=today)
           saveReason.save()
        userdetails=selector.get_email_details(accno)
        if userdetails:
            title=userdetails[3]
            name=userdetails[1]
            email=userdetails[0]
            email=userdetails[0]
            emailservice.SendFinalApprovalEmail(title,name,email,accno)
            
        
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Temperory approval
def temperory_approval(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=int(request.session.get('UserId'))
        accno=request.POST.get('formacc')
        print("Account no",accno)
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        status=selector.get_docs_verified_poi(accno)
        poastatus=selector.get_docs_verified_poa(accno)
        poadocverified=1
        POAstatus=""
        if poastatus:
            poadocverified=poastatus[0]
            POAstatus=poastatus[3]
        print("Status=========",status)
        docverified=1
        POIstatus=""
        if status:
            docverified=status[0]
            POIstatus=status[3]
        if ((docverified==0 or POIstatus=="Not Verified") and (poadocverified==0 or POIstatus=="NotVerified")):
            message="POI and POA is mandatory for temporary approval"
        else:
           message=selector.tmpApproveClient(user,server,password,accno,userid,request)
        
        userdetails=selector.get_email_details(accno)
        if userdetails:
           
            title=userdetails[3]
            name=userdetails[1]
            email=userdetails[0]
            acctype=userdetails[9]
            emailservice.SendTempAccountDetails(title,name,email,accno,acctype)
            
        
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Approval
def approval(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=int(request.session.get('UserId'))
        accno=request.GET.get('account')
        ticket=request.GET.get('ticket')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        client_area=request.GET.get('clientarea')
        print("Approval from=======",userid,accno,user,server,password,client_area)
        status=selector.get_docs_verified_poi(accno)
        print("Status=======",status)
        print("Status=========",status[3])
        docverified=1
        POIstatus=""
        if status:
            docverified=status[0]
            POIstatus=status[3]
        if docverified==0 or POIstatus=="Not Verified":
            message="POI is mandatory for temporary approval"
        else:
            message=selector.approve_live_Client(user,server,password,accno,userid,client_area)
            today=datetime.today()
            one_week=datetime.today()+timedelta(days=7)
            saveReason=TblActionreasons(ticket=ticket,login=accno,action="",duedate=one_week,reason="",userid=userid,status="",updated=today)
            saveReason.save()
            print("Messageeeeeeeeeeeeeeeee",message)
            userdetails=selector.get_email_details(accno)
            if userdetails:
            
                title=userdetails[3]
                name=userdetails[1]
                email=userdetails[0]
                acctype=userdetails[9]
                emailservice.SendLiveAccountDetails(title,name,email,accno,acctype)
            
        
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Email Bank Details
def email_bank_details(request):
    if 'UserId' in request.session:
        print("Email bank details===")
        message="Please try again"
        accno=request.GET.get('account')
        # bankname=request.GET.get('name')
        # address=request.GET.get('address')
        # beneficiary=request.GET.get('beneficiary')
        # swift=request.GET.get('swift')
        # iban=request.GET.get('iban')
        # ffc=request.GET.get('ffc')
        # print("Email Bank account")
        userdetails=selector.get_email_details(accno)
        if userdetails:
           
            title=userdetails[3]
            name=userdetails[1]
            email=userdetails[0]
        emailservice.sendBankDetails(title,name,email)
        message="Email send successfully"
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Terminate Account
def terminate_account(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=int(request.session.get('UserId'))
        accno=request.GET.get('account')
        reasonid=request.GET.get('reasonId')
        description=request.GET.get('description')
        status="Terminated"
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        print("data====",accno,reasonid,description,status,userid)
        # status=selector.get_docs_verified(accno)
        # docverified=1
        # PORstatus=""
        # if status:
        #     docverified=status[0]
        #     PORstatus=status[3]
        message=selector.rejectdocument(accno,reasonid,description,status,userid,user,server,password)

        userdetails=selector.get_email_details(accno)
        if userdetails:
            title=userdetails[3]
            name=userdetails[1]
            email=userdetails[0]
            
            emailservice.terminationofaccount(title,name,email,reasonid)
            
        
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Send email template
def email_template(request):
    if 'UserId' in request.session:
        message="Please try again"
        accno=request.GET.get('account')
        template=request.GET.get('template')
        repname=request.GET.get('repname')
        print("Account no=====",accno,template)
        userdetails=selector.get_email_details(accno)
        if userdetails:
           
            title=userdetails[3]
            name=userdetails[1]
            email=userdetails[0]
            print("Details===",title,name,email,template)
            emailservice.sendtemplate(title,name,email,template,repname)
        message="Email send successfully"
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Dashboard
def backoffice_dashboard(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
        data=selector.dashboard_selector(userid)
        
        return render(request,"backoffice/dashboard.html",data)
    else:
        return redirect('/login')
#Load Transactions
def backoffice_transactions(request):
    if 'UserId' in request.session:
        userid=request.session.get('UserId')
       
        return render(request,"backoffice/transactions.html")
    else:
        return redirect('/login')
#save creditin 
def save_creditIn_information(request):
    if 'UserId' in request.session:
        message="Please try again"
        message=service.save_transactions(request)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')

#History Load
def load_credit_history(request):
    if 'UserId' in request.session:
        data=[]
        userid=request.session.get('UserId')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        accno=int(request.GET.get('account'))
        fromdate=request.GET.get('fromdate')
        todate=request.GET.get('todate')
        print("data====",user,server,password,accno,fromdate,todate)
        row_details,showdetail=selector.history_dll_call(user,server,password,accno,fromdate,todate)
        return JsonResponse({"datalist":row_details,"showdata":showdetail})
    else:
        return redirect('/login')
#Credit Load
def load_credit(request):
    if 'UserId' in request.session:
        data=[]
        userid=request.session.get('UserId')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        accno=int(request.GET.get('account'))
        duplicates=selector.duplicate_account(accno)
        print("Load credit======",user,server,password,accno)
        report=selector.get_wallet_transactions(accno)
        data,datalist,showData=selector.load_credit_dllcall(user,server,password,accno)
        ebalance=selector.loadEwalletBalance(accno)
        print("Send data========",report)

        return JsonResponse({"datas":data,"datalist":datalist,"showdata":showData,"duplicates":duplicates,'wallet':report,'ebalance':ebalance})
    else:
        return redirect('/login')
#deposit in wallet
def deposit_in_wallet(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=request.session.get('UserId')
        message=service.update_ewallet_transactions(request)
     
        # if(result=="success"):
        
        #         currency=userdetails[5]
        #         if status=="creditin":
        #             emailservice.SendCreditInConfirmation(title,name,email,accno,currency,amount)
        #             message="Credit In completed successfully"
        #         if status=="creditout":
        #             emailservice.SendCreditOutConfirmation(title,name,email,accno,currency,amount)
        #             message="Credit Out completed successfully"
        return JsonResponse({"message":message})
    else:
        return redirect('/login')
#Load all Transaction details
def load_all_transaction_details(request):
    if 'UserId' in request.session:
        data={}
       
        accno=request.GET.get('accno')
        
        return JsonResponse({"datas":data})
    else:
        return redirect('/login')

# Transactions history
def transactions_history(request):
    if 'UserId' in request.session:
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        report,opening,closing=selector.get_ewallet_equityreport("","",4,"")

        row_details,showdetail,fromdate,todate=selector.get_mt4_transhistory(user,server,password,"","")
        return render(request,"backoffice/transactionhistory.html",{'reports':report,'opening':opening,'closing':closing,'rowdetails':row_details,'showdetail':showdetail,'from':fromdate,'to':todate})
    else:
        return redirect('/login')
# Transactions history json load
def transactions_history_search(request):
    if 'UserId' in request.session:
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        transtype=int(request.GET.get('type'))
        print("From====",from_date,to_date,transtype)
        report,opening,closing=selector.get_ewallet_equityreport(from_date,to_date,transtype,"")
        
        return JsonResponse({"reports":report})
    else:
        return redirect('/login')


def ewallet_report(request):
    if 'UserId' in request.session:
        accno=request.GET.get('login')
        report,fromdate,todate=selector.get_ewallet_report(accno)
        print("Report====",report)
        return render(request,"backoffice/ewalletreport.html",{"reports":report,"accno":accno,'from':fromdate,'to':todate})
    else:
        return redirect('/login')
def history_ewallet_report(request):
    if 'UserId' in request.session:
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        transtype=request.GET.get('transaction')
        print("Fromdate====",from_date,to_date)
        if(from_date==" " and to_date==" "):
            print("Iside ifff")
            report,opening,closing=selector.get_ewallet_equityreport("","",4,"")
        else:
            if transtype:
                transtype=int(transtype)
            else:
                transtype=2
            report,opening,closing=selector.get_ewallet_equityreport(from_date,to_date,transtype,"")
        return render(request,"backoffice/historyewalletreport.html",{'reports':report,'opening':opening,'closing':closing,'from':from_date,'to':to_date})
    else:
        return redirect('/login')
#MT4 history 
def mt4_transaction_history(request):
    if 'UserId' in request.session:
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        transtype=request.GET.get('type')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        print("Fromdate====",from_date,to_date)
        row_details,showdetail,fromdate,todate=selector.get_mt4_transhistory(user,server,password,from_date,to_date)
        output_dict = [x for x in row_details if transtype in x['COMMENT'] ]
        return JsonResponse({"showdetail":showdetail,"filter":output_dict})
    else:
        return redirect('/login')
#Inter account transfer
def inter_account_transfer(request):
    if 'UserId' in request.session:
        message="Please try again"
        message=service.interaccount_transfer(request)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')
#World Check
def world_check(request):
    if 'UserId' in request.session:
        return render(request,'backoffice/worldchek.html')
    else:
        return redirect('/login')
#IB Page
def affiliates(request):
    if 'UserId' in request.session:
        date_today=datetime.today().date()    
        date_today=date_today.strftime("%Y-%m-%d")
        affiliates=selector.get_affiliates("1900-01-01",date_today,"Live")
        pending=selector.get_affiliates("1900-01-01",date_today,"Pending")
        rejected=selector.get_affiliates("1900-01-01",date_today,"Rejected")
        return render(request,'backoffice/ib.html',{'affiliates':affiliates,'from':"1900-01-01",'to':date_today,'pending':pending,'rejected':rejected})
    else:
        return redirect('/login')
#IB load
def affiliates_load(request):
    if 'UserId' in request.session:
        status=request.GET.get('status')
        from_date=request.GET.get('from')
        to_date=request.GET.get('to')
        data=selector.get_affiliates(from_date,to_date,status)
        return JsonResponse(data,safe=False)
    else:
        return redirect('/login')

def affiliate_details(request):
    if 'UserId' in request.session:
          return render(request,'backoffice/affiliatedetails.html')
    else:
        return redirect('/login')
def affiliate_client_details(request):
    if 'UserId' in request.session:
        login=request.GET.get('login')
        print("Login=====",login)
        clients_data,second_data=selector.get_clients_list(login)
        return render(request,'backoffice/ibclients.html',{'firsts':clients_data,'seconds':second_data})
    else:
        return redirect('/login')
def generatereport(request):
    if 'UserId' in request.session:
        month_data=request.GET.get('month')
        month=0
        year=0
        if month_data:
            dates=month_data.split("-")
            month=int(dates[0])
            year=int(dates[1])
        print("Month and year=====",month,year)
        monthlydata=selector.generate_report_monthly(month,year)
        # print("Type of ===",monthlydata)
        return render(request,'backoffice/reports.html',{'datas':monthlydata})
    else:
        return redirect('/login')
def generate_login_report(request):
    if 'UserId' in request.session:
        month_data=request.GET.get('month')
        login=request.GET.get('login')
        print("Month====Login",month_data,login)
        month=0
        year=0
        if month_data:
            dates=month_data.split("-")
            month=int(dates[0])
            year=int(dates[1])
        print("Month and year=====",month,year)
        all_details=selector.generate_report_monthly_agent(month,year,login)
        
        return render(request,'backoffice/reports.html',{'datas':all_details})
    else:
        return redirect('/login')
#Score
def get_score(request):
    if 'UserId' in request.session:
        login=request.GET.get('login')
        qns=selector.get_score_info()
        print("Questions====",qns)
     
        return render(request,'backoffice/score.html',{'qns':qns})
    else:
        return redirect('/login')
#Client Categorization======
def client_categorisation(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=request.session.get('UserId')
        login=request.GET.get('login')
        category=request.GET.get('category')
        print("Details=====",userid,login,category)
        message=selector.save_client_category(userid,login,category)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')

