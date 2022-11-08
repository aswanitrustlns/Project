from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from .views import *
urlpatterns=[
    path('CaseReport',case_report,name="CaseReport"),
    path('CaseRegister',case_register,name="CaseRegister"),
    path('CaseFilter',case_datefilter,name="CaseFilter"),
    path("CaseSave",save_case,name="CaseSave"),
    path('CRFDetails',detailed_page,name="CRFDetails"),
    path('DocView',view_document,name="DocView"),
    path('StatusUpdate',change_status,name="StatusUpdate"),
    path('ReOpenCase', reopen_case,name="ReoOpenCase"),
    path('CaseFile',case_file_upload,name="CaseFile")
    # path('UserInfo',login_user_info,name="UserInfo")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='CRF'