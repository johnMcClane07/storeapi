# Generated by Django 5.1.1 on 2024-10-10 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_amount',
        ),
    ]
