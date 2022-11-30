from django.db import models

# Create your models here.
class TblClients(models.Model):
    login = models.IntegerField(db_column='Login', primary_key=True)  # Field name made lowercase.
    ticket = models.CharField(db_column='Ticket', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    groups = models.CharField(db_column='Groups', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.IntegerField(db_column='Country', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    zip = models.IntegerField(db_column='Zip', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone = models.TextField(db_column='Phone', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.TextField(db_column='Email', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    idno = models.CharField(db_column='IDNo', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    leverage = models.IntegerField(db_column='Leverage')  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    taxrate = models.FloatField(db_column='TaxRate', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='Enabled', blank=True, null=True)  # Field name made lowercase.
    mqid = models.CharField(db_column='MQID', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    color = models.IntegerField(db_column='Color', blank=True, null=True)  # Field name made lowercase.
    agent = models.IntegerField(db_column='Agent', blank=True, null=True)  # Field name made lowercase.
    readonly = models.IntegerField(db_column='ReadOnly', blank=True, null=True)  # Field name made lowercase.
    sendreports = models.IntegerField(db_column='SendReports', blank=True, null=True)  # Field name made lowercase.
    changepwd = models.IntegerField(db_column='ChangePwd', blank=True, null=True)  # Field name made lowercase.
    otp = models.IntegerField(db_column='OTP', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ipassword = models.CharField(db_column='IPassword', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ppassword = models.CharField(db_column='PPassword', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    referencecode = models.CharField(db_column='ReferenceCode', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mothername = models.CharField(db_column='MotherName', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mothermaidenname = models.CharField(db_column='MotherMaidenName', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nationality = models.IntegerField(db_column='Nationality', blank=True, null=True)  # Field name made lowercase.
    language = models.IntegerField(db_column='Language', blank=True, null=True)  # Field name made lowercase.
    subscribed = models.IntegerField(db_column='Subscribed', blank=True, null=True)  # Field name made lowercase.
    livestatus = models.CharField(db_column='LiveStatus', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy', blank=True, null=True)  # Field name made lowercase.
    dob = models.CharField(db_column='DOB', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    annualincome = models.FloatField(db_column='AnnualIncome', blank=True, null=True)  # Field name made lowercase.
    networth = models.FloatField(db_column='Networth', blank=True, null=True)  # Field name made lowercase.
    initialdeposit = models.FloatField(db_column='InitialDeposit', blank=True, null=True)  # Field name made lowercase.
    profession = models.CharField(db_column='Profession', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    risk = models.CharField(db_column='Risk', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    riskcategory = models.IntegerField(db_column='RiskCategory', blank=True, null=True)  # Field name made lowercase.
    acc_types = models.IntegerField(db_column='Acc_types', blank=True, null=True)  # Field name made lowercase.
    email2 = models.CharField(db_column='Email2', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    readonlycomments = models.TextField(db_column='ReadOnlyComments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    terminatedcomments = models.TextField(db_column='TerminatedComments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    salesrep = models.IntegerField(db_column='SalesRep', blank=True, null=True)  # Field name made lowercase.
    country2 = models.IntegerField(db_column='Country2', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    red = models.IntegerField(db_column='Red', blank=True, null=True)  # Field name made lowercase.
    blue = models.IntegerField(db_column='Blue', blank=True, null=True)  # Field name made lowercase.
    green = models.IntegerField(db_column='Green', blank=True, null=True)  # Field name made lowercase.
    terminated = models.IntegerField(db_column='Terminated', blank=True, null=True)  # Field name made lowercase.
    tin_no = models.CharField(db_column='TIN_NO', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    docsverified = models.IntegerField(db_column='DocsVerified', blank=True, null=True)  # Field name made lowercase.
    stickynotes = models.TextField(db_column='StickyNotes', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reassignedrep = models.IntegerField(db_column='ReassignedRep', blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    converteddate = models.DateTimeField(db_column='ConvertedDate', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
    passportno = models.CharField(db_column='PassportNo', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    us_citizen = models.IntegerField(db_column='US_Citizen', blank=True, null=True)  # Field name made lowercase.
    us_choice = models.IntegerField(db_column='US_Choice', blank=True, null=True)  # Field name made lowercase.
    approvaldate = models.DateTimeField(db_column='ApprovalDate', blank=True, null=True)  # Field name made lowercase.
    approvedby = models.CharField(db_column='ApprovedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    riskstatus = models.IntegerField(db_column='RiskStatus', blank=True, null=True)  # Field name made lowercase.
    not_use_homephone = models.IntegerField(blank=True, null=True)
    currency = models.CharField(db_column='Currency', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    riskassmntdate = models.DateTimeField(db_column='RiskAssmntDate', blank=True, null=True)  # Field name made lowercase.
    preapproveddate = models.DateTimeField(db_column='PreApprovedDate', blank=True, null=True)  # Field name made lowercase.
    preapprovedby = models.CharField(db_column='PreApprovedBy', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rejecteddate = models.DateTimeField(db_column='RejectedDate', blank=True, null=True)  # Field name made lowercase.
    rejectedby = models.CharField(db_column='RejectedBy', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    referral_code = models.CharField(db_column='Referral_Code', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    affiliateid = models.CharField(db_column='AffiliateID', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isaffiliate = models.IntegerField(db_column='IsAffiliate', blank=True, null=True)  # Field name made lowercase.
    terminateddate = models.DateTimeField(db_column='TerminatedDate', blank=True, null=True)  # Field name made lowercase.
    terminatedby = models.CharField(db_column='TerminatedBy', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    countrycategory = models.CharField(db_column='CountryCategory', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    actypecategory = models.CharField(db_column='AcTypeCategory', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    actypedate = models.DateTimeField(db_column='AcTypeDate', blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    closedby = models.CharField(db_column='ClosedBy', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    closedcomments = models.TextField(db_column='ClosedComments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ibid = models.IntegerField(db_column='IBID', blank=True, null=True)  # Field name made lowercase.
    isib = models.IntegerField(db_column='IsIB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_Clients'
    
class TblUser(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    userlogin = models.CharField(db_column='UserLogin', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    designationid = models.IntegerField(db_column='DesignationId', blank=True, null=True)  # Field name made lowercase.
    isonline = models.IntegerField(db_column='IsOnline')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_User'
        

class TblTicketlogs(models.Model):
    logid = models.IntegerField(db_column='LogId')  # Field name made lowercase.
    logtime = models.DateTimeField(db_column='LogTime')  # Field name made lowercase.
    userlogin = models.IntegerField(db_column='Userlogin', blank=True, null=True)  # Field name made lowercase.
    logdata = models.TextField(db_column='LogData', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    chattype = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ticket = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    department = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    username = models.CharField(db_column='Username', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_TicketLogs'


class TblSaleslead(models.Model):
    ticket_no = models.CharField(db_column='Ticket_No', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    name = models.TextField(db_column='Name', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phone1 = models.TextField(db_column='Phone1', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone2 = models.TextField(db_column='Phone2', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email1 = models.TextField(db_column='Email1', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email2 = models.TextField(db_column='Email2', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.TextField(db_column='City', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    zipcode = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    source = models.TextField(db_column='Source', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='Ext', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fax = models.TextField(db_column='Fax', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    salesrepid = models.IntegerField(db_column='SalesRepID', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
    potential = models.IntegerField(db_column='Potential', blank=True, null=True)  # Field name made lowercase.
    transferredfrom = models.IntegerField(db_column='TransferredFrom', blank=True, null=True)  # Field name made lowercase.
    reassignedid = models.IntegerField(db_column='ReassignedID', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    occupation = models.CharField(db_column='Occupation', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country2 = models.CharField(db_column='Country2', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    resolvedcount = models.IntegerField(db_column='ResolvedCount')  # Field name made lowercase.
    hyperlinks = models.CharField(db_column='Hyperlinks', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    experience = models.IntegerField(db_column='Experience')  # Field name made lowercase.
    hear_from = models.CharField(db_column='Hear_From', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    reassignedperc = models.IntegerField(db_column='ReassignedPerc')  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    appform = models.IntegerField(db_column='AppForm', blank=True, null=True)  # Field name made lowercase.
    language = models.IntegerField(db_column='Language', blank=True, null=True)  # Field name made lowercase.
    clientarealogin = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    resolvecomments = models.TextField(db_column='ResolveComments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    resolvedby = models.CharField(db_column='ResolvedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    accountno = models.IntegerField(blank=True, null=True)
    meeting_counter = models.IntegerField(db_column='Meeting_Counter', blank=True, null=True)  # Field name made lowercase.
    prior_act = models.IntegerField(db_column='Prior_Act', blank=True, null=True)  # Field name made lowercase.
    scoring = models.FloatField(db_column='Scoring', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dob = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    subject = models.TextField(db_column='Subject', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    converteddate = models.DateField(db_column='ConvertedDate', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    nationality = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    annualincome = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    networth = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    seminars = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    attending = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    noemail = models.IntegerField(blank=True, null=True)
    sms = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    maybe = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    inquirycomments = models.TextField(db_column='InquiryComments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    salesrep = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    reassignedrep = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ip = models.CharField(db_column='IP', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ibid = models.IntegerField(db_column='IBID', blank=True, null=True)  # Field name made lowercase.
    training = models.CharField(db_column='Training', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_SalesLead'
    
class TblEwalletTransaction(models.Model):
    accnt_no = models.IntegerField()
    amount = models.FloatField()
    trans_type = models.IntegerField()
    trans_date = models.DateTimeField()
    trans_status = models.IntegerField()
    trans_id = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    ewalletid = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(db_column='Remarks', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updated_date = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_eWallet_Transaction'  




