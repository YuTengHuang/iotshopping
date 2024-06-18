from django.contrib import admin
from .models import ProductSpec, Spec, Color

admin.site.register(ProductSpec)
admin.site.register(Spec)
admin.site.register(Color)