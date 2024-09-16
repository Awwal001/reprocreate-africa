from django.urls import path
from store.order_views import *


urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('', OrderCreateView.as_view(), name='order-create'),
    path('<str:tracking_number>', OrderDetailView.as_view(), name='order-detail'),
]
