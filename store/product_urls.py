from django.urls import path
from store.product_views import *

urlpatterns = [
    path('',getProducts, name="products"),
    path('categories', getCategories, name='categories'),

    path('create',createProduct, name="product-create"),
    path('upload',uploadImage, name="image-upload"),


    path('admin',getAdminProducts, name='admin-products'),
    path('<slug:slug>',getProduct, name="Product"),
    path('category/<str:pk>',getproductsByCategory, name="products-category"),

    path('update/<str:pk>',updateProduct, name="product-update"),
    path('delete/<str:pk>',deleteProduct, name="product-delete"),
]