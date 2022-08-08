from unicodedata import name
from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns=[
    path('login/',login,name="Login"),
    path('login_check',login_check,name="Check"),
    path('dashboard/',dashboard,name="Dashboard"),
    path('Leads/',lead,name="Leads"),
    path('LeadRegistration/',lead_registration,name="LeadRegistration"),
    path('LeadSubmit',lead_registration_check,name="LeadSubmit"),
    path('LeadProcessing',lead_processing,name="LeadProcessing"),
    path('logout',logout,name="Logout")
   
 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Admin'