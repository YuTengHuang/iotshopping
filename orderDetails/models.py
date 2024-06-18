from django.db import models
from order.models import Order

class OrderDetails(models.Model):
    oid = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, related_name='OrderDetails')
    product_name = models.CharField(max_length=255, blank=True, null=True)   
    color = models.CharField(max_length=255,blank=True, null=True)
    spec = models.CharField(max_length=255,blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"{self.oid.uid.member_username} - {self.oid.order_trackid}"