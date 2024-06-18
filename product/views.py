from django.http import Http404, HttpResponse
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes

from .models import Product
from .serializers import ProductSerializers, ProductSimpleInfoSerializers
from django.utils import timezone

##################################################  前期教學測試用
class LateProductList(GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]   ## 新增權限讓未驗證者僅允許讀取 這是ProductInformation class底下所有方法都是IsAuthenticatedOrReadOnly
                                                       ## 若沒設置將用setting設置的權限
    def get(self, request):
        product = self.get_queryset()
        serializer = self.serializer_class(product, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

@api_view(['GET'])                                       # 這是用裝飾器方式讓方法變屬性
@permission_classes([IsAuthenticatedOrReadOnly])  
def late_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializers(products, many=True)
    return JsonResponse(serializer.data, safe=False)  ## Response會自動將字典或列表序列化為 JSON 字符串 // JsonResponse 是接收JSON格式
####################################################  前期教學測試用


## 取得活動簡易商品資訊
@api_view(["GET"])
@permission_classes([])
def get_product_simple_info(request):
    products = Product.objects.all()
    curTime = timezone.now().date()
    data = []
    for product in products:
        if product.product_active_at is None and product.product_inactive_at is None:
            continue
        if curTime >= product.product_active_at and curTime <= product.product_inactive_at:
            serializer = ProductSimpleInfoSerializers(product)
            data.append(serializer.data)
    return JsonResponse(data, safe=False)

## 取得簡易全部商品資訊
@api_view(["GET"])
@permission_classes([])
def get_product_page_info(request):
    product = Product.objects.all()
    serializer = ProductSimpleInfoSerializers(product, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)
