from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import RegisterForm
from .models import Member, Address
from .serializers import MemberSerializer, AddressSerializer
from rest_framework import status


@api_view(['GET'])
def userinfo(request):
    member = Member.objects.get(pk=request.user.id)
    username = member.get_member_username()
    email = member.get_username()
    return JsonResponse({
        'id': request.user.id,
        'username': username,
        'email': email,
        "nikename": member.member_nickname
    })



@api_view(['POST'])
@authentication_classes([])  ## 身分驗證
@permission_classes([])      ## 權限限制
def signup(request):
    data = request.data
    message = 'success'
    if Member.objects.filter(member_email=data.get('email')).exists():
        return JsonResponse({"message": "該用戶名的用戶已存在。"})
    
    form = RegisterForm({
        'member_username': data.get('username'),  
        'member_email': data.get('email'),     
        'password1': data.get('password'), 
        'password2': data.get('password2')
    })

    if form.is_valid():
        form.save()
    else: 
        password_errors = []
        if 'password' in form.errors:
            password_errors = form.errors['password']
            print("1", password_errors)

        if 'password2' in form.errors:
            password_errors = form.errors['password2']
            print("2", password_errors)
            
        error_msg = "" 
        for error_msg in password_errors:
            print("password2 錯誤訊息：", error_msg)
            
        message = error_msg 

    return JsonResponse({"message": message})



@api_view(["GET"])
def member_get_data(request):
    address = Address.objects.get(related_member=request.user.id)
    member = Member.objects.get(pk=request.user.id)
    data = {
        "member_username": member.member_username,
        "member_email": member.member_email,
        "member_nickname": member.member_nickname,
        "phone": address.phone,
        "recipient": address.recipient,
        "postal_code": address.postal_code,
        "address": address.address,
        "address_default": address.default,
    }
    return JsonResponse(data)


@api_view(["POST"])
def Order_get_MemberAddr(request):
    address = Address.objects.get(related_member=request.user.id)
    member = Member.objects.get(pk=request.user.id)
    data = {
        "id": member.id,
        "member_username": member.member_username,
        "member_email": member.member_email,
        "phone": address.phone,
        "recipient": address.recipient,
        "postal_code": address.postal_code,
        "address": address.address,
        "address_default": address.default,
    }
    return JsonResponse(data)


@api_view(["POST"])
def member_set_data(request):
    try:
        address = Address.objects.get(related_member=request.user.id)
        member = Member.objects.get(pk=request.user.id)
    except (Address.DoesNotExist, Member.DoesNotExist):
        return JsonResponse({"error": "會員或地址不存在"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.id == member.id:
        member.member_username = request.data.get("member_username", member.member_username)
        member.member_email = request.data.get("member_email", member.member_email)
        member.member_nickname = request.data.get("member_nickname", member.member_nickname)
        member.save()
        
        address.phone = request.data.get("phone", address.phone)
        address.recipient = request.data.get("recipient", address.recipient)
        address.postal_code = request.data.get("postal_code", address.postal_code)
        address.address = request.data.get("address", address.address)
        address.default = request.data.get("address_default", address.default)
        address.save()
        
        m_serializer = MemberSerializer(member)
        a_serializer = AddressSerializer(address)
        return JsonResponse({"member": m_serializer.data, "address": a_serializer.data})
    else:
        return JsonResponse({"error": "信箱與會員信箱不相符"}, status=status.HTTP_400_BAD_REQUEST)
    

from member.task import send_email
from django.core.exceptions import ObjectDoesNotExist

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def sendEmail(request):

    email = request.data.get("email")

    try:
        user = Member.objects.get(member_email=email)
        send_email.delay(user.member_email, user.id)

        return JsonResponse({"msg": "success"})
    except ObjectDoesNotExist:
        return JsonResponse({"msg": "error"})
    except Exception as e:
        return JsonResponse({"msg": "意外"+e})


## 修改密碼
from django.conf import settings
import jwt

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def resetPassword(request):
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')
    token = request.headers.get('Authorization')
    token = token.split(' ')[1]
    if new_password != new_password2:
        return JsonResponse({"msg":"error"})
    
    else:

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = Member.objects.get(id=payload['user_id'])
            user.set_password(new_password)
            user.save()
            return JsonResponse({"msg": "Password reset successfully"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
