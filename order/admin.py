from django.contrib import admin
from .models import Order
# Register your models here.

class OderManager(admin.ModelAdmin):
    list_display = ( "order_trackid", "username", "get_order_status_display",)
    # list_display_links =("username",)   將username指定為點擊連結, 而不是上述第一個

    def username(self, obj):
        return obj.uid.member_username


admin.site.register(Order, OderManager)