from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
urlpatterns = [
    path('userinfo/', views.userinfo, name='userinfo'),
    path('signup/', views.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('member/create-data/', views.member_set_data, name='member_set_data'),
    path('member/get/', views.member_get_data, name='member_get_data'),
    path('order/addr/', views.Order_get_MemberAddr, name='Order_get_MemberAddr'),
    path('sendemail/', views.sendEmail, name='sendEmail'),
    path('resetpassword/', views.resetPassword, name='resetPassword'),
]