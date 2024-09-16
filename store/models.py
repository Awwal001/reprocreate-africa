from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import authentication.models
from central.base_model import BaseModel
from central.constants import STATE_CHOICES
from django.utils.translation import gettext_lazy as _
import authentication

User = get_user_model()


class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)

class CoverImage(models.Model):
    thumbnail = models.URLField(max_length=500)
    original = models.URLField(max_length=500)
    file_name = models.CharField(max_length=255)

class Logo(models.Model):
    thumbnail = models.URLField(max_length=500)
    original = models.URLField(max_length=500)
    file_name = models.CharField(max_length=255)

class Settings(models.Model):
    contact = models.CharField(max_length=20)
    website = models.URLField(max_length=500)
    notifications = models.JSONField(null=True, blank=True)
    location = models.JSONField(null=True, blank=True)
    socials = models.JSONField(null=True, blank=True)


class Shop(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cover_image = models.OneToOneField(CoverImage, on_delete=models.CASCADE)
    logo = models.OneToOneField(Logo, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE)
    orders_count = models.IntegerField()
    products_count = models.IntegerField()


class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    icon = models.CharField(max_length=255, null=True, blank=True)
    image = models.JSONField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    products_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # TODO
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):  # Show name as the identifying field
        return self.name


class ProductImage(BaseModel):
    original = models.URLField(max_length=500)
    thumbnail = models.URLField(max_length=500)



class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    status = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    image = models.OneToOneField(ProductImage, on_delete=models.CASCADE)
    gallery = models.ManyToManyField(ProductImage, related_name='product_gallery')
    ratings = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    total_reviews = models.IntegerField(null=True, blank=True)
    rating_count = models.JSONField(null=True, blank=True)
    my_review = models.JSONField(null=True, blank=True)
    in_wishlist = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)
    tags = models.JSONField(null=True, blank=True)
    metas = models.JSONField(null=True, blank=True)
 


    def save(self, *args, **kwargs):
        # TODO
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):  # Show name as the identifier
        return "{} --> Pharmacy : {} ".format(
            self.name, self.shop.owner
        )


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rating)

# Shipping Address Model
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line if missing
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.zip_code}, {self.country}"



class Order(models.Model):
    tracking_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sales_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, blank=True)
    cancelled_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cancelled_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cancelled_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)
    coupon_id = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    shop = models.ForeignKey('Shop', on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_gateway = models.CharField(max_length=50)
    altered_payment_gateway = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.ForeignKey(authentication.models.Address, on_delete=models.CASCADE)  # Changed to ForeignKey
    logistics_provider = models.CharField(max_length=50, null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.tracking_number} - Product {self.product.name}"

