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
    path('newaccounts',new_accounts,name="NewAccounts"),
    path('Leads/',lead,name="Leads"),
    path('LoadAll',lead_load_all,name="LoadAll"),
    path('duplicate',lead_duplicate_check,name="Duplicate"),
    path('viewMerge',view_merge,name="ViewMerge"),
    path('LeadRegistration/',lead_registration,name="LeadRegistration"),
    path('LeadSubmit',lead_registration_check,name="LeadSubmit"),
    path('LeadProcessing',lead_processing,name="LeadProcessing"),
    path('pendingtickets',pending_tickets,name='PendingTickets'),
    path('load_all_pending',pending_tckts_load_all,name="PendingTktsAll"),
    path('resolvedtickets',resolved_tickets,name='ResolvedTickets'),
    path('load_all_resolved',resolved_tckts_load_all,name="ResolvedTktsAll"),
    path('logout',logout,name="Logout")
   
 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Admin'