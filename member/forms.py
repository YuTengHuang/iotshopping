from django.contrib.auth.forms import UserCreationForm
from .models import Member


class RegisterForm(UserCreationForm):

    class Meta:
        model = Member
        fields = (
            'member_username', 
            'member_email', 
            'password1', 
            'password2'
        )