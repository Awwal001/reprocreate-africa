import os
import jwt
import logging
from .utils import Util
from django.urls import reverse
from django.conf import settings
from .renderers import UserRenderer
from .models import User, UserProfile
from rest_framework.response import Response
from django.http import HttpResponsePermanentRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status, views, permissions
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from .serializers import ( 
    UserRegisterionSerializer, GoogleSocialAuthSerializer, LoginSerializer, LogoutSerializer, UserProfileSerializer,
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, EmailVerificationSerializer, EmailVerificationRequestSerializer
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GoogleSocialAuthView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterionSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        logger.debug(f"Received registration request with data: {request.data}")
        user = request.data
        serializer = self.serializer_class(data=user)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            logger.debug(f"User registered successfully: {user_data}")
            return Response(user_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        logger.debug(f"Received login request with data: {request.POST}")
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            logger.debug('Login successful for user: %s', serializer.validated_data['email'])
            return response
        except Exception as e:
            logger.error('Login failed: %s', str(e))
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RequestEmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        firstname = user.full_name.split(' ')[0]

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        abs_url = f'http://{current_site}{relative_link}?token={token}'
        email_body = f'Hi {firstname}, use the link below to verify your email: {abs_url}'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response({'success': 'We have sent you a link to verify your email'}, status=status.HTTP_200_OK)


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(pk=payload['user_id'])
            if not user.email_verified:
                user.email_verified = True
                user.save()
            return Response({'success': 'Your email has been verified'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
            

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            # redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid password reset token, request a new one'})
            
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):  # Change this to post instead of patch
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logger.debug(f"Received logout request with data: {request.data}")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)