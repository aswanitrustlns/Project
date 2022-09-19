from unicodedata import name
from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns=[
    path('login/',login,name="Login"),
    path('login_check',login_check,name="Check"),
    path('dashboard/',dashboard,name="Dashboard"),
    # path('salesdashboard/',salesdashboard,name="SalesDashboard"),
    # path('newaccounts',new_accounts,name="NewAccounts"),
    path('Leads/',lead,name="Leads"),
    path('LoadAll',lead_load_all,name="LoadAll"),
    path('duplicate',lead_duplicate_check,name="Duplicate"),
    path('viewMerge',view_merge,name="ViewMerge"),
    path('createticket',create_ticket,name="CreateTicket"),
    path('LeadRegistration',lead_registration,name="LeadRegistration"),
    path('NewAccounts',new_accounts,name="NewAccounts"),
    path('LeadSubmit',lead_registration_check,name="LeadSubmit"),
    path('LeadProcessing',lead_processing,name="LeadProcessing"),
    path('Pendingtickets',pending_tickets,name='PendingTickets'),
    path('load_all_pending',pending_tckts_load_all,name="PendingTktsAll"),
    path('Resolvedtickets',resolved_tickets,name='ResolvedTickets'),
    path('load_all_resolved',resolved_tckts_load_all,name="ResolvedTktsAll"),
    path('dormant',dormant_ticket,name="DormantTicket"),
    path('SendReminder',sendRemiderMail,name="SendReminder"),
    path('CancelMail',sendCancelMail,name="CancelMail"),
    path('Meeting',manage_meeting,name="Meeting"),
    path('assessment',meetingScore,name="Score"),
    path('ViewDocument',viewDocument,name="ViewDocument"),
    path('saveScore',saveMeeting,name='SaveMeeting'),
    path('MeetingRequest',send_meeting_request,name="MeetingRequest"),
    path('FeedbackUpdate',update_feedback,name='FeedbackUpdate'),
    path('LoadFuns',viewLoadFunctions,name="LoadFuns"),
    path('AssignRep',assign_rep,name="AssignRep"),
    path('NameSearch',name_search,name="NameSearch"),
    path('MailSearch',mail_search,name="MailSearch"),
    path('PhoneSearch',phone_search,name="PhoneSearch"),
    path('AssessmentUpdate',update_meetingassessment,name="AssessmentUpdate"),
    # path('TicketStatus',ticket_status,name="TicketStatus"),
    # path('AccountStatus',account_status,name="AccountStatus"),
    path('TemplateEmail',send_email_templates,name="TemplateEmail"),
    path('TicketUpdate',ticket_status,name="TicketUpdate"),
    path('AccountUpdate',account_status,name="AccountUpdate"),
    path('ReminderSave',save_reminder_details,name="ReminderSave"),
    path('StickyUpdate',update_sticky_notes,name="StickyUpdate"),
    path('ComposeMail',email_send,name="ComposeMail"),
    path('TicketResolve',resolve_tickets,name="TicketResolve"),
    path('ActivityLog',activity_log,name="ActivityLog"),
    
    #seminar=============================================================
    path('Upcoming',upcomingSeminars,name="Upcoming"),
    path('RegisterSeminar',registerSeminars,name="RegisterSeminar"),
    path("SeminarUpdate",updateseminar,name="SeminarUpdate"),
    path('AllSeminar',list_all_seminar,name="AllSeminar"),
    path("OpenDemo",open_demoaccount,name="OpenDemo"),
    # path('ChangeMeeting',change_meeting_request,name="ChangeMeeting"),
    path('livelogs',liveChatLogs,name="LiveLogs"),
    path('Inbox',emailInbox,name="Inbox"),
    path('Read',emailRead,name="Read"),
    path("sendItems",send_items_list,name="sendItems"),
    path('ReadSendItems',read_send_items,name="ReadSendItems"),
    path('logout',logout,name="Logout")
   
 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Admin'