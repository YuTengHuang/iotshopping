from django.urls import path
from shopcart import views


urlpatterns = [
    path("shop/postdata/", views.post_data),
    path("shop/getdata/", views.get_data),
    path("shop/plusItem/", views.plusItem),
    path("shop/minusItem/", views.minusItem),
    path("shop/DeleteiTem/", views.DeleteiTem),
    path("shop/getlength/", views.get_length),
]