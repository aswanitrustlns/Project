from django.db import connection
import string
import random
from django.template.loader import render_to_string
class Selector: 
    def generatepassword(self):
        try:
           master_pwd=random_pwd_gen()
           investor_pwd=random_pwd_gen()
           phone_pwd=random_pwd_gen()
           
        except Exception as e:
            print("Exception----",e)
        return master_pwd,investor_pwd,phone_pwd
           
   
#Random password generator
def random_pwd_gen():
        all = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.sample(all,8))
        return password