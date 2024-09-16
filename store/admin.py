from django.contrib import admin
from . models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(Address)
admin.site.register(CoverImage)
admin.site.register(Logo)
admin.site.register(ProductImage)
admin.site.register(Settings)
admin.site.register(Shop)