from django.db import models
from member.models import Member
from product.models import Product
from product_spec.models import Color, Spec
from django.dispatch import receiver
from django.db.models.signals import pre_delete

class ShopCart(models.Model):
    uid = models.ForeignKey(Member, verbose_name=("Member"), on_delete=models.CASCADE, related_name='ShopCart')
    pid = models.ForeignKey(Product, verbose_name=("Product"), on_delete=models.CASCADE)
    cid = models.ForeignKey(Color, verbose_name=("Color") , on_delete=models.SET_NULL, blank=True, null=True)
    sid = models.ForeignKey(Spec, verbose_name =("Spec") , on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"{self.uid.member_username} - {self.pid.product_name}"

@receiver(pre_delete, sender=Color)  ## (signals訊號)(receiver接收): 當Color的某資料被刪除後, 找到有此值的購物車資料並刪除
def delete_shop_cart_on_color_delete(sender, instance, **kwargs):
    ShopCart.objects.filter(cid=instance).delete()

@receiver(pre_delete, sender=Spec)
def delete_shop_cart_on_spec_delete(sender, instance, **kwargs):
    ShopCart.objects.filter(sid=instance).delete()