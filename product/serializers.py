from rest_framework import serializers
from .models import Product
imgaddress = 'http://127.0.0.1:8000'
class ProductSerializers(serializers.ModelSerializer):

    get_url = serializers.SerializerMethodField('_get_url') 

    get_image = serializers.SerializerMethodField()      
    
    get_thumbnail = serializers.ReadOnlyField()            
                                                            
    get_image2 = serializers.SerializerMethodField()                                                        
    get_image3 = serializers.SerializerMethodField()                                                        

    class Meta:
        model = Product
        # fields = '__all__' 
        fields = (
            'product_id',
            'product_name',
            'product_active_at',
            'product_inactive_at',
            'product_price',
            'product_desc',
            'get_url',
            'get_image',  
            'get_image2',
            'get_image3',
            'get_thumbnail',
        )

    def _get_url(self, product_obj):  
        slug = getattr(product_obj, "slug")  
        return f'/{slug}/'
    
    def get_get_image(self, obj):       
        if obj.product_image: 
            return imgaddress + obj.product_image.url
        return ''
    
    def get_get_image2(self, obj):       
        if obj.product_image2: 
            return imgaddress + obj.product_image2.url
        return ''
    
    def get_get_image3(self, obj):     
        if obj.product_image3: 
            return imgaddress + obj.product_image3.url
        return ''


class ProductSimpleInfoSerializers(serializers.ModelSerializer):

    get_url = serializers.SerializerMethodField('_get_url')

    class Meta:
        model = Product
        fields=(
            'product_id',
            'product_name',
            'product_active_at',
            'product_inactive_at',
            'product_price',
            'get_url',
            'get_thumbnail',
        )

    def _get_url(self, product_obj):  
        slug = getattr(product_obj, "slug")
        return f'/{slug}/'
