from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from .views import *
urlpatterns=[
     path('seminars',view_seminars,name="Seminars"),
     path('AddEn',add_button_click,name="AddEn"),
     path('Info',get_webinar_info,name="Info"),
     path("Delete",delete_seminar,name="Delete"),
     path("Update",edit_button_click,name="Update"),
     path('SeminarReport',view_seminar_report,name="SeminarReport"),
     path('LoadSeminar',report_load,name="LoadSeminar"),
     path('ViewOpened',view_opened_account,name="ViewOpened"),
     path('AttendanceUpdate',update_account,name="AttendanceUpdate"),
     path('Confirmation',seminar_confirmation,name="Confirmation"),
     path('LoadConfirmation', confirmation_grid,name="LoadConfirmation"),
     path('RegistrationSeminar',registerSeminars,name="RegistrationSeminar"),
     path('EmailTemplate',send_email_templates,name="EmailTemplate"),
     path('AttendeesPrint',print_attendees,name="AttendeesPrint"),
     path('UpcomingDetails',upcoming_details,name="UpcomingDetails")
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Seminars'