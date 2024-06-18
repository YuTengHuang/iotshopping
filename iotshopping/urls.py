from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('member.urls')),
    path('api/', include('product.urls')),
    path('api/', include('product_spec.urls')),
    path('api/', include('shopcart.urls')),
    path('api/', include('order.urls')),
    path('api/', include('orderDetails.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
