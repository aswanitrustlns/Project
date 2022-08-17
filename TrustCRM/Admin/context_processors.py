  #Sales Performers of the month
from django.db import connection

def get_sales_performers(request):
        try:
            Cursor=connection.cursor()
            Cursor.execute("set nocount on;exec SP_TopPerformers_PY")
            performers=Cursor.fetchall()
            funded=sorted(performers,key=lambda i:i[2],reverse=True)
            live=sorted(performers,key=lambda i:i[3],reverse=True)
            spoken=sorted(performers,key=lambda i:i[4],reverse=True)
            updated=sorted(performers,key=lambda i:i[5],reverse=True)            
            # top_performer={'funded':funded,'live':live,'spoken':spoken,'updated':updated}
        except Exception as e:
            print("Exception---",e)
        finally:
            Cursor.close()
        return {'funded':funded,'live':live,'spoken':spoken,'updated':updated}


        