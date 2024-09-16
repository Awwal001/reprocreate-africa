from rest_framework import serializers
from .models import Product, Category
from users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderProduct, ShippingAddress, Review, Category, ProductImage
from authentication.models import Address
import random
import string



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'original', 'thumbnail']

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    image = ProductImageSerializer() 
    gallery = ProductImageSerializer(many=True) 

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    
    # def get_images(self, obj):
    #     images = obj.productimage_set.all()
    #     serializer = ReviewSerializer(images, many=True)
    #     return serializer.data


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderProducts = OrderProductSerializer(source='order_products', many=True, read_only=True)
    shippingAddress = AddressSerializer(source='shipping_address', read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_user(self, obj):
        return {
            "id": obj.customer.id,
            "email": obj.customer.email,
            "fullname": obj.customer.full_name,
        }

    def generate_tracking_number(self):
        """Generate a random tracking number."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def create(self, validated_data):
        # Extract order items from request data
        order_items = self.context['request'].data.get('orderItems', [])
        
        print("Order Items: ", order_items)  # Debugging line

        # Generate random tracking number
        validated_data['tracking_number'] = self.generate_tracking_number()

        # Create the order instance
        order = super().create(validated_data)

        # (1) Create order items and link them to the order
        for item_data in order_items:
            product = Product.objects.get(id=item_data['product'])

            print(f"Creating OrderProduct for Product {product.name} with qty {item_data['qty']}")  # Debugging line

            # Create the OrderProduct instance
            order_product = OrderProduct.objects.create(
                product=product,
                order=order,
                order_quantity=item_data['qty'],
                unit_price=item_data['price'],
                subtotal=item_data['qty'] * item_data['price']
            )

            # (2) Update product stock
            product.quantity -= order_product.order_quantity
            if product.quantity < 0:
                raise serializers.ValidationError(f"Product {product.name} is out of stock!")
            product.save()

            print(f"OrderProduct {order_product.id} created successfully.")  # Debugging line

        return order




class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_products(self, obj):
        products = obj.product_set.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data