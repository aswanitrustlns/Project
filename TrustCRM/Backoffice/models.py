from django.db import models

# Create your models here.

class TblActionreasons(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ticket = models.CharField(db_column='Ticket', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    login = models.IntegerField(db_column='Login', blank=True, null=True)  # Field name made lowercase.
    action = models.TextField(db_column='Action', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    reason = models.TextField(db_column='Reason', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    updated = models.DateTimeField(db_column='Updated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_ActionReasons'

class TblScorecalcQns(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    question = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    section = models.CharField(db_column='Section', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_ScoreCalc_qns'
    def __unicode__(self):
        return u'%s' % (self.title)

class TblScorecalcOpt(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    options = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    value = models.IntegerField()
    score = models.IntegerField()
    qn_id = models.ForeignKey(TblScorecalcQns,on_delete=models.CASCADE,db_column='qn_Id', blank=True, null=True,related_name='qun')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_ScoreCalc_opt'
    def __unicode__(self):
        return u'%s' % (self.title)

class TblScoresheet(models.Model):
    login = models.IntegerField(db_column='Login', primary_key=True)  # Field name made lowercase.
    ai = models.IntegerField(blank=True, null=True)
    msi = models.IntegerField(blank=True, null=True)
    sow = models.IntegerField(blank=True, null=True)
    exfya = models.IntegerField(blank=True, null=True)
    nameofinsti = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    coforigin = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    antiamt = models.IntegerField(blank=True, null=True)
    p_reas = models.IntegerField(blank=True, null=True)
    slye = models.IntegerField(blank=True, null=True)
    past_prof = models.IntegerField(blank=True, null=True)
    tofmar = models.IntegerField(blank=True, null=True)
    fininstr = models.IntegerField(blank=True, null=True)
    finservice = models.IntegerField(blank=True, null=True)
    avganfreq = models.IntegerField(blank=True, null=True)
    avganvol = models.IntegerField(blank=True, null=True)
    finlev = models.IntegerField(blank=True, null=True)
    lev_past = models.IntegerField(blank=True, null=True)
    high_lev = models.IntegerField(blank=True, null=True)
    mar_cfd = models.IntegerField(blank=True, null=True)
    sbc = models.IntegerField(blank=True, null=True)
    otcd = models.IntegerField(blank=True, null=True)
    etd = models.IntegerField(blank=True, null=True)
    avamtotc = models.IntegerField(blank=True, null=True)
    maxlvgqn = models.IntegerField(blank=True, null=True)
    sloqn = models.IntegerField(blank=True, null=True)
    oposqn = models.IntegerField(blank=True, null=True)
    empstatus = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vosia = models.IntegerField(blank=True, null=True)
    psof = models.IntegerField(blank=True, null=True)
    aaat = models.IntegerField(blank=True, null=True)
    foyt = models.IntegerField(blank=True, null=True)
    why_trade = models.IntegerField(blank=True, null=True)
    mop = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mar_status = models.IntegerField(blank=True, null=True)
    leo = models.IntegerField(blank=True, null=True)
    e_status = models.IntegerField(blank=True, null=True)
    no_of_trades = models.IntegerField(blank=True, null=True)
    last_trade = models.IntegerField(blank=True, null=True)
    qn1 = models.IntegerField(blank=True, null=True)
    prior_edu = models.IntegerField(blank=True, null=True)
    qn2 = models.IntegerField(blank=True, null=True)
    qn3 = models.IntegerField(blank=True, null=True)
    qn4 = models.IntegerField(blank=True, null=True)
    annual_income = models.IntegerField(blank=True, null=True)
    fut_exp_amt = models.IntegerField(blank=True, null=True)
    reg_fin_comm = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mtp = models.IntegerField(blank=True, null=True)
    expend_cfd = models.IntegerField(blank=True, null=True)
    len_time = models.IntegerField(blank=True, null=True)
    nat_of_prof = models.IntegerField(blank=True, null=True)
    main_src_income = models.IntegerField(blank=True, null=True)
    est_net_worth = models.IntegerField(blank=True, null=True)
    tot_score = models.FloatField(blank=True, null=True)
    uae = models.IntegerField(blank=True, null=True)
    eg = models.IntegerField(blank=True, null=True)
    fund_method = models.CharField(db_column='Fund_Method', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pep = models.IntegerField(blank=True, null=True)
    completed = models.IntegerField(db_column='Completed', blank=True, null=True)  # Field name made lowercase.
    emp_position = models.IntegerField(blank=True, null=True)
    annual_inc = models.DecimalField(db_column='annual_Inc', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    fund_ctry = models.IntegerField(blank=True, null=True)
    fund_inst = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dep_nex_12 = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    purpose_service = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_avg_lot_fininst = models.IntegerField(blank=True, null=True)
    last_avg_freq_qtr = models.IntegerField(blank=True, null=True)
    prev_trd_lev = models.IntegerField(blank=True, null=True)
    no_yrs_fininst = models.IntegerField(blank=True, null=True)
    rlvnt_qlf_yrs = models.IntegerField(blank=True, null=True)
    qn5 = models.IntegerField(blank=True, null=True)
    pep_desc = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    industry_other = models.TextField(db_column='industry_Other', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    no_yrs_fininstr_desc = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rel_qlf_yrs_desc = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    est_networth_other = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    trade_exp = models.IntegerField(blank=True, null=True)
    tickb1 = models.IntegerField(db_column='TickB1', blank=True, null=True)  # Field name made lowercase.
    tickb2 = models.IntegerField(db_column='TickB2', blank=True, null=True)  # Field name made lowercase.
    tickb3 = models.IntegerField(db_column='TickB3', blank=True, null=True)  # Field name made lowercase.
    tickb4 = models.IntegerField(db_column='TickB4', blank=True, null=True)  # Field name made lowercase.
    spanish = models.IntegerField(db_column='Spanish', blank=True, null=True)  # Field name made lowercase.
    portugal = models.IntegerField(db_column='Portugal', blank=True, null=True)  # Field name made lowercase.
    escore = models.IntegerField(db_column='EScore', blank=True, null=True)  # Field name made lowercase.
    kscore = models.IntegerField(db_column='KScore', blank=True, null=True)  # Field name made lowercase.
    src_income_other = models.CharField(db_column='Src_Income_Other', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    src_income = models.CharField(db_column='Src_Income', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fund_ctry_multi = models.CharField(db_column='fund_ctry_Multi', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    posteddate = models.DateTimeField(db_column='PostedDate', blank=True, null=True)  # Field name made lowercase.
    postedip = models.CharField(db_column='PostedIP', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    us_citizen = models.IntegerField(db_column='US_Citizen', blank=True, null=True)  # Field name made lowercase.
    us_choice = models.IntegerField(db_column='US_Choice', blank=True, null=True)  # Field name made lowercase.
    employername = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    employeraddress = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    annualsalary = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    saving_invst_amount = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    gifts_inherit_amount = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    chinese = models.IntegerField(db_column='Chinese', blank=True, null=True)  # Field name made lowercase.
    tax_ctry = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tax_num = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    hastin = models.IntegerField(blank=True, null=True)
    notinreas = models.IntegerField(blank=True, null=True)
    notin_other = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tin_declare = models.IntegerField(blank=True, null=True)
    account_bonus = models.IntegerField(blank=True, null=True)
    risk_take = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_Scoresheet'
