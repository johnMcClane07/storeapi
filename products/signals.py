from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product
from .tasks import send_emails

@receiver(pre_save, sender=Product)
def cache_old_price(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = sender.objects.get(pk=instance.pk)
        instance._old_price = previous_instance.price
    else:
        instance._old_price = None

@receiver(post_save, sender=Product)
def email(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_old_price'):
        old_price = instance._old_price
        new_price = instance.price

        if old_price is not None and old_price != new_price:
            print(instance.id)
            send_emails.delay(product_id=instance.id, user_email='glazkov.daniil2004@gmail.com')
            print(f"Price changed from {old_price} to {new_price}")
        else:
            print("Price has not changed.")
    
