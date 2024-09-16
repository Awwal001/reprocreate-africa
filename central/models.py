from django.db import models
from central.constants import STATE_CHOICES
from django.contrib.auth import get_user_model
from store.models import Product
from django.utils.text import slugify
from django.db import models
from central.base_model import BaseModel

User = get_user_model()

# class School(BaseModel):
#     name = models.CharField(max_length=300, null=True, blank=True)
#     slug = models.SlugField(blank=True, null=True)
#     address = models.CharField(max_length=300, null=True, blank=True)

#     def number_of_products(self):
#         product_count = Product.objects.filter(school=self)
#         return product_count.count()

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(School, self).save(*args, **kwargs)

#     def __str__(self):  # Show title as the identifier
#         return self.name


class Contact(BaseModel):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()


class Bookmark(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)

