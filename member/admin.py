from django.contrib import admin
from .models import Address

from django.contrib.auth import get_user_model
Member = get_user_model()
admin.site.register(Member)
admin.site.register(Address)
