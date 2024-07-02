from rest_framework import serializers
from .models import Product
imgaddress = 'http://127.0.0.1:8000'
class ProductSerializers(serializers.ModelSerializer):

    get_url = serializers.SerializerMethodField('_get_url') # 方法一 在序列化建立方法並使用

    get_image = serializers.SerializerMethodField()         # 方法二 在序列化建立方法 SerializerMethodField() 不加東西 它會預設查找底下 get_<前面取的變數名稱>的方法 (get_get_image)
    # image = serializers.SerializerMethodField()           # 方法2.5 若不用get_image當名稱 改用image 這樣預設就會查找get_<前面取的變數名稱>方法 (get_image)
     
    get_thumbnail = serializers.ReadOnlyField()             # 方法三 使用ReadOnlyField() 讀取有標記 @property 的方法(請見models.py) 僅傳回字段的值而不進行修改
                                                            # 若有多個方法被標記則需指定 ReadOnlyField(source = "指定方法名")

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
            'get_image',      #<<<<<<<<< 這邊改成"image"，方法2.5就OK
            'get_image2',
            'get_image3',
            'get_thumbnail',
        )

    def _get_url(self, product_obj):   # 方法一  product_obj是隨意取的, 他將根據 Meta的model來抓取(物件)
        slug = getattr(product_obj, "slug")   # 新增變數 並用getattr(物件, 物件的屬性) 附值
        return f'/{slug}/'
    
    def get_get_image(self, obj):          # 方法二 同上只是不用getattr
        if obj.product_image: 
            return imgaddress + obj.product_image.url
        return ''
    
    def get_get_image2(self, obj):          # 方法二 同上只是不用getattr
        if obj.product_image2: 
            return imgaddress + obj.product_image2.url
        return ''
    
    def get_get_image3(self, obj):          # 方法二 同上只是不用getattr
        if obj.product_image3: 
            return imgaddress + obj.product_image3.url
        return ''
    
    # def get_image(self, obj):              # 方法 2.5 同上只是不用getattr
    #     if obj.product_image: 
    #         return 'http://127.0.0.1:8000' + obj.product_image.url
    #     return ''


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

    def _get_url(self, product_obj):   # 方法一  product_obj是隨意取的, 他將根據 Meta的model來抓取(物件)
        slug = getattr(product_obj, "slug")   # 新增變數 並用getattr(物件, 物件的屬性) 附值
        return f'/{slug}/'