from django.urls import path
from . import views
urlpatterns = [
    path('OrderDetails/', views.OrderDetailsView.as_view(), name='OrderDetails'),
]

### Rest Api