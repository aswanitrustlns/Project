from unicodedata import name
from django.urls import URLPattern, path
from .views import *
urlpatterns=[
    path('login/',login,name="Login"),
    path('login_check',login_check,name="Check"),
    path('dashboard/',dashboard,name="Dashboard"),
    path('Leads/',lead,name="Leads"),
    path('LeadRegistration/',lead_registration,name="LeadRegistration"),
    path('logout',logout,name="Logout")
   
 
]
app_name='Admin'