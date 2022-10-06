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
     path("Delete",delete_seminar,name="Delete")
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
app_name='Seminars'