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
      path('BackofficeUpdate',backoffice_update,name="BackofficeUpdate"),
      path('Approval',bank_approval,name="Approval"),
      path('CardDetails',load_card_data,name="CardDetails"),
      path('ApproveCard',approve_card,name="ApproveCard"),
      path('ApproveBank',approve_bank,name="ApproveBank"),
      path('SaveCard',save_card,name="SaveCard"),
      path('BankDetails',load_bankaccount_details,name="BankDetails"),
      path('SaveBankAccount',save_bank_account,name="SaveBankAccount"),
      path('Cryptodetails',load_crypto_data,name="Cryptodetails"),
      path('CryptoSave',save_bank_account,name="CryptoSave")

     
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Backoffice'