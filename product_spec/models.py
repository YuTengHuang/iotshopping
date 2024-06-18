from django.db import models


class Spec(models.Model):
    size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"size - {self.size}"

class Color(models.Model):
    color_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"color - {self.color_name}"

class ProductSpec(models.Model):
    pid = models.ForeignKey("product.Product", verbose_name=("Product"), on_delete=models.CASCADE)
    spec = models.ForeignKey(Spec, verbose_name=("Product Spec"), on_delete=models.CASCADE,blank=True, null=True)
    color = models.ForeignKey(Color, verbose_name=("Color"), on_delete=models.CASCADE, blank=True, null=True)
    product_spec_stock = models.BooleanField(blank=True, null=True, default=True)

    class Meta:
        unique_together = ('pid', 'spec')

    
    def __str__(self):
        if self.spec is None and self.color.color_name is None:
            return f"{self.pid.product_name}"
        elif self.spec is None:
            return f"{self.pid.product_name} - {self.color.color_name}"
        elif self.color is None:
            return f"{self.pid.product_name} - {self.spec.size}"
        else:
            return f"{self.pid.product_name} - {self.spec.size} - {self.color.color_name}"