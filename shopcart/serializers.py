from rest_framework import serializers
from .models import ShopCart

class ShopCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShopCart
        fields = "__all__"