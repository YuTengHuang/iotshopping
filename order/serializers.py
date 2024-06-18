from rest_framework import serializers
from django.utils.timezone import localtime
from .models import Order

class OrderSerializers(serializers.ModelSerializer):
    
    createTime = serializers.SerializerMethodField()

    class Meta:
        model=Order
        fields = '__all__'




    def get_createTime(self, obj):
        return localtime(obj.order_datetime)