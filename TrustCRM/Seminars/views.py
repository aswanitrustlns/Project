from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .services import Services
service=Services()
# Create your views here.
def view_seminars(request):
    print("All seminars========")
    titles=service.get_last_seminar()
    all_seminar=service.get_seminar_info_list()
   
    return render(request,'seminars/eventregistration.html',{'titles':titles,'seminars':all_seminar})
def add_button_click(request):
    print("Add button click")
    service.save_new_event_details(request)
    return JsonResponse({"saved":"success"})
def get_webinar_info(request):
    webinarid=request.GET.get('id')
    webinarinfo=service.view_webinar(webinarid)
    return JsonResponse({"info":webinarinfo})
def edit_button_click(request):
    service.save_new_event_details(request)
    return JsonResponse({"saved":"success"})
def delete_seminar(request):
    id=request.GET.get('id')
    service.delete_seminar(id)
    return JsonResponse({"delete":"success"})

