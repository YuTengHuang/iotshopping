from django.urls import path
from product_spec import views


urlpatterns = [
    path("productInfo/<slug:slug>/", views.get_product_info),
    path("SingleProductCheckOut/<slug:slug>/", views.Single_product_check_out),
]