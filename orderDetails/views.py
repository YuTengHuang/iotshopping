from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from .serializers import OrderDetailsSerializers
from shopcart.models import ShopCart
from order.models import Order
from .models import OrderDetails

class OrderDetailsView(GenericAPIView):

    def post(self, request):

        data = request.data
        message = "error"
        # print("AAAA", data)
        for d in data["cart"]:
            
            form = {
                "oid": data["trackid"],
                "product_name": d["product_name"],
                "color": d["color"],
                "spec": d["spec"],
                "price": d["product_price"],
                "quantity": d["quantity"],
            }
            serializer = OrderDetailsSerializers(data=form)
            if serializer.is_valid():
                serializer.save()
                message = "success"
            else:
                message = "error"
                return JsonResponse({"message":message})

        shopcarts = ShopCart.objects.filter(uid=request.user.id)
        shopcarts.delete()
        
        return JsonResponse({"message":message})
    
    def get(self, request):

        order = Order.objects.filter(uid=request.user.id).last()

        detail = OrderDetails.objects.filter(oid=order.order_trackid)

        res = OrderDetailsSerializers(detail, many=True)

        return JsonResponse(res.data, safe=False)