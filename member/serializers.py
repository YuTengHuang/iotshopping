from member.models import Member, Address
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member  
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'