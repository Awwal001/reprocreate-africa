# Generated by Django 4.1.2 on 2024-08-09 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=20)),
                ('street_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('icon', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.JSONField(blank=True, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('products_count', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoverImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.URLField(max_length=500)),
                ('original', models.URLField(max_length=500)),
                ('file_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.URLField(max_length=500)),
                ('original', models.URLField(max_length=500)),
                ('file_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sales_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('cancelled_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cancelled_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cancelled_delivery_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('language', models.CharField(max_length=10)),
                ('coupon_id', models.IntegerField(blank=True, null=True)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_gateway', models.CharField(max_length=50)),
                ('altered_payment_gateway', models.CharField(blank=True, max_length=50, null=True)),
                ('logistics_provider', models.CharField(blank=True, max_length=50, null=True)),
                ('delivery_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_time', models.CharField(max_length=50)),
                ('order_status', models.CharField(max_length=50)),
                ('payment_status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sku', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('in_stock', models.BooleanField(default=True)),
                ('status', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('ratings', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('total_reviews', models.IntegerField(blank=True, null=True)),
                ('rating_count', models.JSONField(blank=True, null=True)),
                ('my_review', models.JSONField(blank=True, null=True)),
                ('in_wishlist', models.BooleanField(default=False)),
                ('tags', models.JSONField(blank=True, null=True)),
                ('metas', models.JSONField(blank=True, null=True)),
                ('categories', models.ManyToManyField(to='store.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('original', models.URLField(max_length=500)),
                ('thumbnail', models.URLField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=20)),
                ('website', models.URLField(max_length=500)),
                ('notifications', models.JSONField(blank=True, null=True)),
                ('location', models.JSONField(blank=True, null=True)),
                ('socials', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('orders_count', models.IntegerField()),
                ('products_count', models.IntegerField()),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.address')),
                ('cover_image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.coverimage')),
                ('logo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.logo')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('settings', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.settings')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='gallery',
            field=models.ManyToManyField(related_name='product_gallery', to='store.productimage'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.productimage'),
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.shop'),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.shippingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.shop'),
        ),
    ]
