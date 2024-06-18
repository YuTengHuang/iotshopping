from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Member
@shared_task
def send_email(recipient_email, user_id): 
    
    user = Member.objects.get(id=user_id) 

    token = RefreshToken.for_user(user).access_token
    absurl = 'http://localhost:5173/inputresetpassword/?token='+str(token)
    subject = '重製密碼'

    html_content = f'''
    <p>您好，{user.member_username}</p>
    <p>請點擊以下連結重設密碼：</p>
    <p><a href="{absurl}">{absurl}</a></p>
    '''

    msg = EmailMultiAlternatives(
        subject,
        "some text",
        settings.EMAIL_HOST_USER, # 寄件人的信箱
        [recipient_email] # 收件人的信箱
    )
    
    msg.attach_alternative(html_content, "text/html")
    mail_sent = msg.send()

    if mail_sent:
        return "success"
    else:
        return "error"