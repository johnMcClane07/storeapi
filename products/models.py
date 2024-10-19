from django.db import models
from .tasks import recalculate_final_price

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    discount=models.IntegerField()
    description = models.TextField()
    final_price=models.IntegerField(null=True,blank=True)
    category=models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount=self.discount
        self.__price=self.price
    
    def save (self, *args, **kwargs):
        if self.discount != self.__discount or self.price != self.__price:
            recalculate_final_price.delay(self.id)
        super().save(*args, **kwargs)

class ProductImages(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='images/')

class Category(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()





