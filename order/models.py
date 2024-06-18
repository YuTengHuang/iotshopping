from django.db import models
from member.models import Member
from django.utils import timezone

class Order(models.Model):
    DELIVERED = True
    IN_DELIVERED = False
    status_choices = [
        (DELIVERED, "已送達"),
        (IN_DELIVERED, "配送中")
    ]

    uid = models.ForeignKey(Member, verbose_name=("Member"), on_delete=models.CASCADE, related_name='Order')
    order_trackid = models.CharField(max_length=255, editable=False, primary_key=True)
    order_datetime = models.DateTimeField(default=timezone.now, editable=False)
    order_recipient_name = models.CharField(max_length=255, blank=True, null=True)
    order_recipient_address = models.CharField(max_length=255, blank=True, null=True)
    order_phone = models.CharField(max_length=10, blank=True, null=True)
    order_tel = models.CharField(max_length=10, blank=True, null=True)
    order_postal_code = models.CharField(max_length=3, blank=True, null=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    order_status = models.BooleanField(default=IN_DELIVERED, choices=status_choices)
    order_note = models.CharField(max_length=255, blank=True, null=True)    


    def __str__(self):
        return f"{self.uid.member_username} - {self.order_trackid}"


    def save(self, *args, **kwargs):
        if not self.order_trackid:
            time = timezone.localtime(self.order_datetime)
            self.order_trackid = f"{time.strftime('%Y%m%d%H%M%S')}{self.uid.id}"
        super().save(*args, **kwargs)