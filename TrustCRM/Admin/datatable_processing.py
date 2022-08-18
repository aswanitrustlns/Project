
from django_serverside_datatable.views import ServerSideDatatableView
from django.db import connection
from datetime import datetime, timedelta

class ItemListView(ServerSideDatatableView):
    def get_load_all(self,userId):
        try:
                Cursor=connection.cursor()    
                date_today=datetime.today().date()   
                date_today=date_today.strftime("%Y-%m-%d")
                Cursor.execute("exec SP_GetSalesLeadsListPaginate_PY %s,%s,%s,%s,%s",[userId,"1900-01-01",date_today,'P',0])
                _tickets=Cursor.fetchall()  
                columns = ['Date', 'Email', 'Name','Phone','Source','Country']
        except Exception as e:
                print("Exception----",e)
        finally:
                Cursor.close()


# urls.py
# add the following line to urlpatterns

# path('data/', views.ItemListView.as_view()), 