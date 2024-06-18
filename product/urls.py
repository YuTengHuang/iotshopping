from django.urls import path
from product import views as pv


urlpatterns = [
    # path('product/', pv.LateProductList.as_view()), # 沒用裝飾器用法
    path('product/', pv.late_product_list),           # 裝飾器用法
    path('productsimpleinfo/', pv.get_product_simple_info),
    path('productpageinfo/', pv.get_product_page_info)
]
