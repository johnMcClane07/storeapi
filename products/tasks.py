from celery import shared_task
from django.core.mail import send_mail



@shared_task
def recalculate_final_price(product_id):
    from products.models import Product
    print(f"Запуск пересчета финальной цены для продукта с ID: {product_id}")
    try:
        product = Product.objects.get(id=product_id)

        # Рассчитываем скидку и финальную цену
        discount = product.price * (product.discount / 100)
        final_price = product.price - discount

        if final_price != product.final_price:
            product.final_price = final_price
            product.save(force_update=True)

        print(f"Финальная цена для продукта '{product.name}' пересчитана: {final_price}")
    except Product.DoesNotExist:
        print(f"Продукт с id {product_id} не найден.")

@shared_task
def send_emails(product_id,user_email='glazkov.daniil2004@gmail.com'):
    print(f"Sending email for product with ID: {product_id}")
    try:
        from products.models import Product
        from userprofile.models import Favourite
        product = Product.objects.get(id=product_id)
        recipient_list = [favourite.user.email for favourite in Favourite.objects.filter(product_id=product.id).select_related('user')]
        if not recipient_list:
            print("No recipients found. Skipping sending email.")
            return
        if not product:
            print("Product not found. Skipping sending email.")
            return
        product_data = {'id': product.id, 'name': product.name}
        send_mail(subject=f'Hi, we have some news for you!',
                message=f'We have a new product from your favourites for sale: {product_data["name"]}',
                from_email='glazkov.daniil2004@gmail.com',
                recipient_list=recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")
