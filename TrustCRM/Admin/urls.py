from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from .views import *
urlpatterns=[
    path('login/',login,name="Login"),
    path('login_check',login_check,name="Check"),
    path('dashboard/',dashboard,name="Dashboard"),
    # path('salesdashboard/',salesdashboard,name="SalesDashboard"),
    # path('newaccounts',new_accounts,name="NewAccounts"),
    path('index.html', TemplateView.as_view(template_name="test/index.html")),
    path('Leads',lead,name="Leads"),
    path('LoadAll',lead_load_all,name="LoadAll"),
    path('LeadClick',lead_load_click,name="LeadClick"),
    path('duplicate',lead_duplicate_check,name="Duplicate"),
    path('viewMerge',view_merge,name="ViewMerge"),
    path('createticket',create_ticket,name="CreateTicket"),
    path('LeadRegistration',lead_registration,name="LeadRegistration"),
    path('NewAccounts',new_accounts,name="NewAccounts"),# Navigate to new accounts page
    path('NewAccountsPend',new_accounts_pend,name="NewAccountsPend"),
    path('ExtAccounts',existing_accounts,name='ExtAccounts'),
    path('ExtClick',ext_accounts_funded_click,name='ExtClick'),
    path('NewAccountsClick',new_accounts_click,name="NewAccountsClick"),# Get New Accounts Page clicks
    path('NewAccountsFundedClick',new_accounts_funded_click,name="NewAccountsFundedClick"),# Get New Accounts Page Funded clicks
    path('AccountsFilter',new_accounts_variants,name="AccountsFilter"),
    path('WeeklyFilter',new_accounts_variants_weekly,name="WeeklyFilter"),
    path('LeadSubmit',lead_registration_check,name="LeadSubmit"),
    path('LeadProcessing',lead_processing,name="LeadProcessing"),
    path('Pendingtickets',pending_tickets,name='PendingTickets'),
    path('PendingSummary',pending_tickets_from_summary,name="PendingSummary"),
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
    path('csvUpload',upload_csv_file,name="csvUpload"),
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
    path('TicketLogs',ticket_logs_insertion,name="TicketLogs"),
    path('SalesReport',get_sales_report,name="SalesReport"),
    path('Report',get_sales_report_date,name="Report"),
    path('PrintReport', print_sales_call_report,name="PrintReport"),
    path('MonthlyReport',get_sales_report_monthly,name="MonthlyReport"),
    path('Livechat',live_chat,name="Livechat"),
    path('InactiveLoad',inactiveticketLoad,name="InactiveLoad"),
    path('Campaigns',salescampaigns,name="Campaigns"),
    path('SelectCampaign',load_sales_campaign,name="SelectCampaign"),
    path('MissedChat',missed_live_chat,name="MissedChat"),
    path('Funded',funded_accounts,name="Funded"),
    
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
    path("BacksendItems",send_items_list_backoffice,name="BacksendItems"),
    path("SalessendItems",send_items_list_sales,name="SalessendItems"),
    path("SupportsendItems",send_items_list_support,name="SupportsendItems"),
    path('ReadSendItems',read_send_items,name="ReadSendItems"),
    path('ReadBackofficeSendItems',read_backoffice_send_items,name="ReadBackofficeSendItems"),
    path('ReadSalesSendItems',read_sales_send_items,name="ReadSalesSendItems"),
    path('ReadSupportSendItems',read_support_send_items,name="ReadSupportSendItems"),
    path('EmailData',email_data,name="EmailData"),
    path('Calendar',show_calendar,name="Calendar"),
    path('Events',show_events,name="Events"),
    path('TicketSummary',ticket_summary,name="TicketSummary"),
    path('TicketSummaryOnLoad',ticket_summary_onload,name="TicketSummaryOnLoad"),
    path("InactiveTickets",inactivetickets,name="InactiveTickets"),
    path('LivechatReport',livechatreport,name="LivechatReport"),
    path('AllLivechatReport',livechatreport_load_all,name="AllLiveChatReport"),
    #Compliance============================================================
    # path('ComplianceDashboard',compliance_dashboard,name="ComplianceDashboard"),
    path('ComplianceDetails',complaint_details,name="ComplianceDetails"),
    path('AllComplaints',detailed_complaints,name="AllComplaints"),
    path('ComplianceUpdate',complaint_update,name="ComplianceUpdate"),
    path("ComplaintMail",mailto_complaint_client,name="ComplaintMail"),
    path('ManageAccounts',compliance_manage_accounts,name="ManageAccounts"),
    #Automation===============================================================
    path('AutomateManager',assign_to_manager,name="AutomateManager"),
    path('AutomateRep',remind_rep_nonfunded,name="AutomateRep"),
  
    path('logout',logout,name="Logout"),
    
   
 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Admin'