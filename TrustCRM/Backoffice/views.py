from atexit import register
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .service import Services
from .selector import Selector
from .emailservice import EmailServices

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
       print("Passwords================================",master_pwd,investor_pwd,phone_pwd) 
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
        print("Account number=======",acc_no)
        details=selector.get_bank_details(acc_no)
        print("Details========",details)
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
        print("Back office update====")
        acc_no=request.POST.get('formacc')

        leverage=int(request.POST.get("Leverage"))
        
        category=selector.duplicate_account(acc_no)
        print("category=======",category)
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
        print("Account number=====",accno)
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
        print("Account number=====",accno)
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
        print("Account number=====",accno,id,card,status,cardtype)
        details=selector.verify_redit_card_details(id,accno,status,userid)
        userdetails=selector.get_user_details(accno)
        if userdetails:
            userdetails=userdetails[0]
            title=userdetails[2]
            name=userdetails[1]
            email=userdetails[0]
            emailservice.SendCardApprovalmail(title,name,email,card,cardtype,status)
        print("User details=========",userdetails)
        
        return JsonResponse({"details":details}) 
    else:
        return redirect('/login')
#Approve Bank
def approve_bank(request):
    if 'UserId' in request.session:
        print("Approve bank is here")
        details=""
        status=request.GET.get('status')
        id=request.GET.get('id')
        userid=request.session.get('UserId')
        accno=request.GET.get('accno')
        card=request.GET.get('card')
        
        print("Account number=====",accno,card,status,id)
        details=selector.verify_bank_details(id,accno,status,userid)
        print("Detils-========",details)
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
            print("Count==========",count)
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
        
        print("Save bank account=======")
        message=service.save_bank_account(request)
        return JsonResponse({"message":message}) 
    else:
        return redirect('/login')
#Save Bank account
def save_crypto_account(request):
    if 'UserId' in request.session:
        message=""
        
        print("Save crypto account=======")
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
        print("view card front",id,accno,side)
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
        accno=request.GET.get('account')
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        status=selector.get_docs_verified_poi(accno)
        print("Status=========",status[3])
        docverified=1
        POIstatus=""
        if status:
            docverified=status[0]
            POIstatus=status[3]
        if docverified==0 or POIstatus=="Not Verified":
            message="POI is mandatory for temporary approval"
        else:
           message=selector.tmpApproveClient(user,server,password,accno,userid)
        
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
#Email Bank Details
def email_bank_details(request):
    if 'UserId' in request.session:
        print("Email bank details===")
        message="Please try again"
        accno=request.GET.get('account')
        bankname=request.GET.get('name')
        address=request.GET.get('address')
        beneficiary=request.GET.get('beneficiary')
        swift=request.GET.get('swift')
        iban=request.GET.get('iban')
        ffc=request.GET.get('ffc')
        print("Email Bank account")
        userdetails=selector.get_email_details(accno)
        if userdetails:
           
            title=userdetails[3]
            name=userdetails[1]
            email=userdetails[0]
        emailservice.sendBankDetails(accno,bankname,address,beneficiary,swift,iban,ffc,title,name,email)
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
        userid=request.session.get('UserId')
        accno=request.POST.get('accno')
        status=request.POST.get('status')
        amount=request.POST.get('deposit')
        
        print("Credit UIn========",accno,status)
        result=service.save_transactions(request)
        if(result=="success"):
            userdetails=selector.get_user_details(accno)
            if userdetails:
                userdetails=userdetails[0]
                title=userdetails[2]
                name=userdetails[1]
                email=userdetails[0]
                currency=userdetails[5]
                if status=="creditin":
                    emailservice.SendCreditInConfirmation(title,name,email,accno,currency,amount)
                    message="Credit In completed successfully"
                if status=="creditout":
                    emailservice.SendCreditOutConfirmation(title,name,email,accno,currency,amount)
                    message="Credit Out completed successfully"
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
        data,datalist,showData=selector.load_credit_dllcall(user,server,password,accno)
        return JsonResponse({"datas":data,"datalist":datalist,"showdata":showData,"duplicates":duplicates})
    else:
        return redirect('/login')
#deposit in wallet
def deposit_in_wallet(request):
    if 'UserId' in request.session:
        message="Please try again"
        userid=request.session.get('UserId')
        service.update_ewallet_transactions(request)
     
        # if(result=="success"):
        #     userdetails=selector.get_user_details(accno)
        #     if userdetails:
        #         userdetails=userdetails[0]
        #         title=userdetails[2]
        #         name=userdetails[1]
        #         email=userdetails[0]
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
#Load all Transaction details
def load_transaction_details(request):
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

        row_details,showdetail=selector.get_mt4_transhistory(user,server,password,"","")
        return render(request,"backoffice/transactionhistory.html",{'reports':report,'opening':opening,'closing':closing,'rowdetails':row_details,'showdetail':showdetail})
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
        return render(request,"backoffice/ewalletreport.html")
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
        row_details,showdetail=selector.get_mt4_transhistory(user,server,password,from_date,to_date)
        output_dict = [x for x in row_details if transtype in x['COMMENT'] ]
        return JsonResponse({"showdetail":showdetail,"filter":output_dict})
    else:
        return redirect('/login')
#Inter account transfer
def inter_account_transfer(request):
    if 'UserId' in request.session:
        message="Please try again"
        name=request.GET.get('name')
        balance=request.GET.get('balance')
        margin=request.GET.get('margin')
        credit=0
        account1=request.GET.get('account1')
        account2=request.GET.get('account2')
        amount=request.GET.get('amount')
        initial=request.GET.get('initial')
        comment1="Withdrawal From"+account1
        comment2="Deposit To"+account2
        user=request.session.get('user')
        server=request.session.get('server')
        password=request.session.get('password')
        print("Initial====",initial)
        
        message=service.interaccount_transfer(account1,account2,name,balance,margin,credit,amount,comment2,user,server,password)
        if(initial==1):
            selector.get_live_status(account2,amount)
        else:
            selector.get_live_status(account2,0)
        userdetails=selector.get_user_details(account1)
        if userdetails:
                userdetails=userdetails[0]
                title=userdetails[2]
                name=userdetails[1]
                email=userdetails[0]
                currency=userdetails[5]
        dormant_check=selector.dormant_check(account1)
        if(dormant_check==1):
            emailservice.SendDormant(title,name,email,account2,currency)
        return JsonResponse({"message":message})
    else:
        return redirect('/login')










        

            











