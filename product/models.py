from django.db import models

from io import BytesIO
from PIL import Image
from django.core.files import File

imgaddress = 'http://127.0.0.1:8000'

class Product(models.Model):
    product_id = models.BigAutoField(auto_created=True, primary_key=True)
    product_name = models.CharField(max_length=45)
    product_create_at = models.DateTimeField(auto_now_add=True)
    product_active_at = models.DateField(null=True, blank=True)
    product_inactive_at = models.DateField(null=True, blank=True)
    product_rank = models.IntegerField(null=True, blank=True)
    product_image = models.ImageField(upload_to='static/', blank=True, null=True)
    product_image2 = models.ImageField(upload_to='static/', blank=True, null=True)
    product_image3 = models.ImageField(upload_to='static/', blank=True, null=True)
    product_thumbnail = models.ImageField(upload_to='static/', blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=0, default=9999999999)
    product_desc = models.TextField(max_length=255, null=True, blank=True)
    slug = models.SlugField()
    class Meta:
        ordering = ('-product_create_at',)

    def __str__(self):
        return self.product_name
    
    @property             
    def get_thumbnail(self):                # serializers 方法三  此裝飾器將方法轉換為屬性
        if self.product_thumbnail:
            return imgaddress + self.product_thumbnail.url
        else:
            if self.product_image:
                self.product_thumbnail = self.make_thumb(self.product_image)
                self.save()

                return imgaddress + self.product_thumbnail.url
            
            else:
                return ''
    
    def make_thumb(self, product_image):
        size = (300, 250)

        img = Image.open(product_image)
        img = img.convert('RGB')
        img.thumbnail(size)

        tumbIO = BytesIO() 
        img.save(tumbIO,"JPEG",quality=85)

        tumb = File(tumbIO, name=product_image.name)
        return tumb

