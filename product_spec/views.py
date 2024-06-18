from django.http import Http404
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes

from django.apps import apps

from .models import ProductSpec
from product.serializers import ProductSerializers
from product.models import Product
from django.utils import timezone


def get_slug(slug):
    try:
        product = Product.objects.get(slug=slug)
        product_specs = ProductSpec.objects.filter(pid=product)
        return product_specs
    except ProductSpec.DoesNotExist:
        raise  Http404
    

##  取得商品詳細資訊
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_product_info(request, slug):
    product_specs = get_slug(slug) 

    ## 獲取其主鍵值
    product_ids = [product_spec.pid.pk for product_spec in product_specs]

    all_product_specs = ProductSpec.objects.filter(pid_id__in=product_ids)
    
    products_info_dict = {}

    for product_spec in all_product_specs:
        product_id = product_spec.pid.product_id
        if product_id not in products_info_dict:
            products_info_dict[product_id] = {
                'pid': ProductSerializers(product_spec.pid).data,
                'product_specs': []
            }
        product_info = {
            'product_specs_id': product_spec.id,
            'spec': product_spec.spec.id if product_spec.spec else None,
            'spec_size': product_spec.spec.size if product_spec.spec else None,
            'color': product_spec.color.id if product_spec.color else None,
            'color_color': product_spec.color.color_name if product_spec.color else None,
            'product_spec_stock': product_spec.product_spec_stock
        }
        products_info_dict[product_id]['product_specs'].append(product_info)
    products_info = list(products_info_dict.values())
    
    return JsonResponse(products_info, safe=False)



@api_view(["POST"])
def Single_product_check_out(request, slug):
    curTime = timezone.now().date()
    product = Product.objects.get(slug=slug)
    pid = product.product_id
    size = ''
    color = ''

    if request.data["spec"] != '':
        product_size = ProductSpec.objects.get(pid=pid, spec_id=request.data["spec"])
        size = product_size.spec.size
        
        
    if request.data["color"] != '':    
        product_color = ProductSpec.objects.get(pid=pid, color_id=request.data["color"])
        color = product_color.color.color_name


    if product.product_active_at is None and product.product_inactive_at is None:
        price = product.product_price

    elif curTime >= product.product_active_at and curTime <= product.product_inactive_at:
        price = float(product.product_price)* 0.5
       
    
    resData = {
        "product_name": product.product_name,
        "product_price": price,
        "spec": size,
        "color": color,
        "quantity": request.data["quantity"]
    }

    return JsonResponse(resData, safe=False)