from rest_framework import serializers
from .models import TblClients,TblSaleslead,TblUser,TblCountry


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=TblCountry
        # fields='__all__'
        fields=['country']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=TblUser
        # fields='__all__'
        fields=['username']

class SalesLeadSerializer(serializers.ModelSerializer):
    
    salesrep=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=TblSaleslead
        # fields='__all__'
        fields=['salesrep']

class ClentsSerializer(serializers.ModelSerializer):
    country=CountrySerializer()
    salesrep=SalesLeadSerializer()
    class Meta:
        model=TblClients
        # fields='__all__'
        fields=['login','regdate','name','email','source','ticket','country','salesrep']