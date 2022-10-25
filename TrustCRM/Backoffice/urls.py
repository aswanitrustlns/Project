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
      path('CryptoSave',save_crypto_account,name="CryptoSave"),
      path('CardView',load_card_front,name="CardView"),
      path('ViewandUploadDocument',view_document,name="ViewandUploadDocument"),
      path('UploadDocumnents',upload_document,name="UploadDocuments"),
      path('LogUpdate',update_log,name="LogUpdate"),
      path('ApproveDocument',approve_document,name="ApproveDocument"),
      path('ExpiryAlert',send_expiry_alert,name='ExpiryAlert'),
      path('ViewDocumentImage',load_document_image,name="ViewDocumentImage"),
      path('MT4password',check_mt4_password,name="MT4password"),
      path('Multipleaccount',multiple_account_create,name="Multipleaccount"),
      path('CommisionStructure',load_commision_structure,name="CommisionStructure"),
      path('ResetPhonePassword',reset_phone_pwd,name="ResetPhonePassword"),
      path('UpdateClientCredential',update_client_area_credential,name="UpdateClientCredential"),
      path('FinalApproval',final_approval,name="FinalApproval"),
      path('TemporaryApproval',temperory_approval,name="TemporaryApproval"),
      path('TicketSummary',summary_ticket,name="TicketSummary"),
      path('JournalUpdate',journal_update,name="JournalUpdate"),
      path('ReminderLoading',load_reminders,name="ReminderLoading"),
      path('EmailBankDetails',email_bank_details,name="EmailBankDetails"),
      path('TerminateAccount',terminate_account,name="TerminateAccount"),
      path('EmailTemplates',email_template,name="EmailTemplates"),
      path('BackofficeDashboard',backoffice_dashboard,name="BackofficeDashboard"),
      path('Transactions',backoffice_transactions,name="Transactions"),
      path('CreditInConfirmation',save_creditIn_information,name="CreditInConfirmation"),
      path('LoadHistory',load_credit_history,name="LoadHistory"),
      path('DepositinWallet',deposit_in_wallet,name="DepositinWallet"),
      path('LoadAllTransaction',load_all_transaction_details,name="LoadAllTransaction"),
      path('LoadTransactions',load_transaction_details,name="LoadTransactions"),
      path('LoadCredit',load_credit,name="LoadCredit"),
      path('TransactionHistory',transactions_history,name="TransactionHistory"),
      path('EWalletReport',ewallet_report,name="EWalletReport"),
      path('HistoryEWalletReport',history_ewallet_report,name="HistoryEWalletReport"),
      path('TransactionHistorySearch',transactions_history_search,name="TransactionHistorySearch"),
      path('MT4TransactionHistory',mt4_transaction_history,name="MT4TransactionHistory")


     
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Backoffice'