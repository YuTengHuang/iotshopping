from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
# from django.contrib.auth.models import User

from django.db.models.signals import post_save
            
class MyUserManager(UserManager):
    def create_user(self,member_email, member_username, password=None, **extra_fields):
        
        if not member_email:
            raise ValueError("電子信箱可能已存在或其他問題!")
        
        member_email = self.normalize_email(member_email)
        user = self.model(member_email=member_email, member_username=member_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, member_email, member_username='admin', password=None, **extra_fields):

        user = self.create_user(member_email, member_username=member_username, password=password)
        user.is_staff = True
        user.is_superuser=True
        user.is_admin = True
        
        user.save(using=self._db)

        return user

class Member(AbstractBaseUser, PermissionsMixin):
    
    member_email = models.EmailField(
       blank=True, default='', unique=True, error_messages={'unique': ("該用戶名的用戶已存在。"),}
    )
    member_username = models.CharField(max_length=45, blank=True, null=True)
    member_nickname = models.CharField(max_length=45, blank=True, null=True)
    member_register = models.DateTimeField(auto_now_add=True)
    member_lastlogin = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'member_email'
    EMAIL_FIELD = 'member_email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-member_register',)

    def __str__(self):
        return str(self.member_email)
    
    def get_member_username(self):
        return self.member_username
    

class Address(models.Model):
    related_member = models.OneToOneField("member.Member", on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    recipient = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=3, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    default = models.BooleanField(blank=True, null=True)

    class Meta:
        ordering = ('related_member',)
    
    def __str__(self):
        return str(self.related_member.member_username)
    
def create_Addr(sender, instance, created, **kwargs):
    if created:
        member_addr = Address(related_member=instance)
        member_addr.save()
        
post_save.connect(create_Addr, sender=Member)