from django.urls import path
from product import views as pv


urlpatterns = [
    path('product/', pv.late_product_list),          
    path('productsimpleinfo/', pv.get_product_simple_info),
    path('productpageinfo/', pv.get_product_page_info)
]
