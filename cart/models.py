from django.db import models

class Cart(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    total_price=models.PositiveIntegerField(default=0)  

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
