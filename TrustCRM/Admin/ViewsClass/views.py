from django.views import View
from datetime import datetime, timedelta

class DashBoardBasedView(View):

    def post(self,request):
        if 'UserId' in request.session:
            UserId=request.session.get('UserId')
            global all_data
            seminar_weekly_pie=[]
            meeting_daily_pie=[]
            meeting_weekly_pie=[]
            daily_live_bar=[]
            weekly_live_bar=[]
            status_bar=[]
            seminar_daily_pie=[]
            halfyearly_bar=[]
            insta_follwers_list=[]
            count=0
            date_today=datetime.today().date()
            week_day=datetime.today().weekday() # Monday is 0 and Sunday is 6
            date_today=date_today.strftime("%Y-%m-%d")
            date_yesterday = datetime.today()-timedelta(1)
            date_yesterday=date_yesterday.strftime("%Y-%m-%d")
            print (date_yesterday)
            