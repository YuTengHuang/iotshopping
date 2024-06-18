from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .serializers import ShopCartSerializers
from .models import ShopCart
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


## 加入購物車
@api_view(["POST"])
def post_data(request):
    data = request.data
    # print(data)

    query = Q(uid=data['uid']) & Q(pid=data["pid"])
    if data.get("cid") != '':
        query &= Q(cid=data["cid"])
    if data.get("sid") != '':
        query &= Q(sid=data["sid"])
    

    existedData = ShopCart.objects.filter(query).first()

    if existedData:
        existedData.quantity += data["quantity"]
        existedData.save()
        message = 'success'
    else:
        serializer = ShopCartSerializers(data=data)

        if serializer.is_valid():
            serializer.save()  
            message = 'success'
        else:
            message = 'error'

    return JsonResponse({"message": message})


## 取得所有購物車資料
@api_view(["POST"])
def get_data(request):
    curTime = timezone.now().date()
    cartDatas = ShopCart.objects.filter(uid=request.user.id).order_by('pid__product_name', '-id')
    res = []
    
    for cartData in cartDatas:
        
        if cartData.pid.product_active_at is None and cartData.pid.product_inactive_at is None:
            price = cartData.pid.product_price
            isActive = False

        elif curTime >= cartData.pid.product_active_at and curTime <= cartData.pid.product_inactive_at:
            price = int(float(cartData.pid.product_price) * 0.5)
            isActive = True
        
        get_url = f"/{cartData.pid.slug}/"
        product_id = cartData.pid.product_id
        spec = cartData.sid.size if cartData.sid else None
        color = cartData.cid.color_name if cartData.cid else None
        totalPrice = price * cartData.quantity

        res_info = {
            'id': cartData.id,
            'pid': product_id,
            'get_thumbnail': cartData.pid.get_thumbnail,
            'product_name': cartData.pid.product_name,
            'totalPrice': totalPrice,
            "product_price": price,
            "spec": spec,
            "color": color,
            "quantity": cartData.quantity,
            "isActive": isActive,
            "get_url": get_url,
        }
    
        res.append(res_info)
            
    return JsonResponse(res, safe=False)


## 取得購物車長度
@api_view(["GET"])
def get_length(request):
    length = 0
    cartDatas = ShopCart.objects.filter(uid=request.user.id)
    for data in cartDatas:
        length += data.quantity
    return JsonResponse({"length": length}) 


## 增加數量
@api_view(["POST"])
def plusItem(request):
    try: 
        shopCartData = ShopCart.objects.get(id=request.data["id"])
        shopCartData.quantity += 1
        shopCartData.save() 
        return JsonResponse({"message": "success"}) 
    except ObjectDoesNotExist:
        return JsonResponse({"error": "無此商品"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


## 減少數量
@api_view(["POST"])
def minusItem(request):

    try:
        shopCartData = ShopCart.objects.get(id=request.data["id"])
        shopCartData.quantity -= 1
        shopCartData.save()
        return JsonResponse({"message": "success"}) 
    except ObjectDoesNotExist:
        return JsonResponse({"error": "無此商品"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


## 刪除數量
@api_view(["DELETE"])
def DeleteiTem(request):
    try:
        shopCartData = ShopCart.objects.get(id=request.data["id"])
        shopCartData.delete()
        return JsonResponse({"message": "success"})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "無此商品"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)