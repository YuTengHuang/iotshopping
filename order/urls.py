from django.urls import path
from . import views
urlpatterns = [
    path('postOrder/', views.postOrder, name='postOrder'),
    path('getOrderid/', views.getOrderid, name='getOrderid'),
    path('getAllOrder/', views.getAllOrder, name='getAllOrder'),
    path('getOneDateils/<slug:trackid>/', views.getOneDateils, name='getAllOrder'),
]