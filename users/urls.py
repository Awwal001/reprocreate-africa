from .views import *
from django.urls import path


urlpatterns = [

    path('', getUsers, name="users"),

    path('me', getMe, name='user'),
    path('<int:pk>', UpdateUserAPIView.as_view(), name='update_user'),
    # path('<int:pk>', RetrieveUserAPIView.as_view(), name='retrieve_user'),
    

    path('<int:pk>', deleteUser, name='user-delete'),
    path('addresses', ListAddressesAPIView.as_view(), name='list_addresses'),
    path('address/create', CreateAddressAPIView.as_view(), name='create_address'),
    path('address/<int:pk>', DeleteAddressAPIView.as_view(), name='delete_address'),
    # path('address/<int:pk>', RetrieveAddressAPIView.as_view(), name='retrieve_address'),
    path('address/update/<int:pk>', UpdateAddressAPIView.as_view(), name='update_address'),
    
]
