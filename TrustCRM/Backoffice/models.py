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
