from .models import ProductSpec
from product.serializers import ProductSerializers
from rest_framework import serializers

class ProductSpecSerializers(serializers.ModelSerializer):
    pid = ProductSerializers()  # 嵌套序列化器
    spec_size = serializers.CharField(source='spec.size', read_only=True)
    color_color = serializers.CharField(source='color.color_name', read_only=True)

    class Meta:
        model = ProductSpec
        # fields = '__all__'
        fields = (
            'pid',
            'spec',
            'spec_size',
            'color',
            'color_color',
            'product_spec_stock',
        )