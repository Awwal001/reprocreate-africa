# Generated by Django 4.1.2 on 2024-09-13 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
