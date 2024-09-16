from authentication.models import User
from users.serializers import  UserSerializer, AddressSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.response import Response
from authentication.models import Address
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMe(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

class RetrieveUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = self.serializer_class(user)
            logger.debug('User retrieved successfully')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f'User with id {pk} not found')
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = self.serializer_class(user, data=request.data, partial=True)  # Note the 'partial=True'
            if serializer.is_valid():
                # Handle password separately if necessary
                if 'password' in request.data:
                    user.password = make_password(request.data['password'])
                
                serializer.save()  # This will now save user and addresses
                
                logger.debug('User updated successfully, including addresses')
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            logger.error('User update validation failed: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            logger.error(f'User with id {pk} not found')
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)




# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateUser(request, pk):
#     user = User.objects.get(id=pk)

#     data = request.data

#     user.full_name = data['name']
#     user.email = data['email']
#     user.is_staff = data['isAdmin']

#     user.save()

#     serializer = UserSerializer(user, many=False)

#     return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')



class CreateAddressAPIView(generics.GenericAPIView):
    serializer_class = AddressSerializer

    def post(self, request):
        logger.debug(f"Received address creation request with data: {request.data}")
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug('Address created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error('Address creation failed: %s', str(e))
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RetrieveAddressAPIView(generics.GenericAPIView):
    serializer_class = AddressSerializer

    def get(self, request, pk):
        try:
            address = Address.objects.get(pk=pk)
            serializer = self.serializer_class(address)
            logger.debug('Address retrieved successfully')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            logger.error(f'Address with id {pk} not found')
            return Response({'detail': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateAddressAPIView(generics.GenericAPIView):
    serializer_class = AddressSerializer

    def put(self, request, pk):
        try:
            address = Address.objects.get(pk=pk)
            serializer = self.serializer_class(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.debug('Address updated successfully')
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error('Address update validation failed: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            logger.error(f'Address with id {pk} not found')
            return Response({'detail': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteAddressAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    lookup_field = 'pk'

    def delete(self, request, pk, *args, **kwargs):
        try:
            address = self.get_object()
            address.delete()
            logger.debug('Address deleted successfully')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            logger.error(f'Address with id {pk} not found')
            return Response({'detail': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

class ListAddressesAPIView(generics.GenericAPIView):
    serializer_class = AddressSerializer

    def get(self, request, user_id):
        addresses = Address.objects.filter(user_id=user_id)
        serializer = self.serializer_class(addresses, many=True)
        logger.debug('Addresses listed successfully')
        return Response(serializer.data, status=status.HTTP_200_OK)
