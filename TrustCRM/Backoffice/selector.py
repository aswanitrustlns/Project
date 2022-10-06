from django.db import connection
class Selector: 
    def generatepassword(self):
        try:
            Cursor=connection.cursor() 
            pass
        except Exception as e:
            print("Exception----",e)
        finally:
            Cursor.close()