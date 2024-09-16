from rest_framework import serializers
from authentication.models import User, UserProfile, Avatar, Address
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['original', 'thumbnail']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['size', 'verified']
    
    def validate_file(self, value):
        # Validate the file size
        if value.size > 1024*1024:  # 1 MB
            raise serializers.ValidationError('File size exceeds 1 MB')
        # Validate the file type
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError('Only PDF files are allowed')
        return value


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=False)
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        user = super().update(instance, validated_data)

        for address_data in addresses_data:
            address_id = address_data.get('id')
            if address_id:
                # Update existing address
                try:
                    address_instance = Address.objects.get(id=address_id, user=user)
                    for key, value in address_data.items():
                        setattr(address_instance, key, value)
                    address_instance.save()
                except Address.DoesNotExist:
                    raise serializers.ValidationError(f"Address with ID {address_id} does not exist.")
            else:
                # Create a new address if no id is provided
                Address.objects.create(
                    user=user,
                    **address_data  # Directly pass address_data here
                )

        return user








    # def get_isAdmin(self, obj):
    #     return obj.is_staff

    # def get_name(self, obj):
    #     name = obj.full_name
    #     if name == '':
    #         name = obj.email
    #     return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True, source='addresses')  # Make sure to use the related name

    class Meta:
        model = User
        fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'