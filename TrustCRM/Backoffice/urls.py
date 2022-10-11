from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from .views import *
urlpatterns=[
      path('Generate',generate_passwords,name="Generate"),
      path('ChangePassword',change_password,name='ChangePassword'),
      path('Change',change_password_request,name="Change"),
      path('Manage',manage_account,name="Manage"),
      path('AccountDetails',load_account_details,name="AccountDetails"),
      path('DuplicateAccount',check_duplicate,name="DuplicateAccount"),
      path('BackofficeUpdate',backoffice_update,name="BackofficeUpdate")
     
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Backoffice'