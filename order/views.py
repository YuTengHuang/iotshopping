from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import OrderSerializers
from orderDetails.models import OrderDetails
from orderDetails.serializers import OrderDetailsSerializers
from .models import Order

@api_view(["POST"])
def postOrder(request):

    data = request.data

    serializer = OrderSerializers(data=data)

    if serializer.is_valid():
        serializer.save()

    order = Order.objects.filter(uid=data["uid"]).last()
    
    trackid = order.order_trackid

    return JsonResponse({"trackid" : trackid})


@api_view(["GET"])
def getOrderid(request):

    order = Order.objects.filter(uid=request.user.id).last()

    serializer = OrderSerializers(order)

    return JsonResponse(serializer.data)



@api_view(["POST"])
def getAllOrder(request):
    orders = Order.objects.filter(uid=request.user.id).order_by('-order_trackid')
    order_serializers = OrderSerializers(orders, many=True)

    for order in order_serializers.data:
        single_order = Order.objects.get(order_trackid=order['order_trackid'])
        order_details = OrderDetails.objects.filter(oid=single_order)
        order['order_details'] = OrderDetailsSerializers(order_details, many=True).data
    

    return JsonResponse({"data": order_serializers.data})


@api_view(["GET"])
def getOneDateils(request, trackid):

    orderData = Order.objects.get(order_trackid=trackid)
    resOrder = OrderSerializers(orderData).data

    detailData = OrderDetails.objects.filter(oid=trackid)
    resDateil = OrderDetailsSerializers(detailData, many=True).data

    resOrder["order_details"] = resDateil

    return JsonResponse(resOrder, safe=False)