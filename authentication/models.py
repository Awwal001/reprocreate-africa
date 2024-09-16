import random
from django. utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from django.db.models.signals import post_save
import store.models



class UserManager(BaseUserManager):

    def create_user(self, full_name, email, username=None, password=None):
        if full_name is None:
            raise TypeError('Users should have a full_name')
        if email is None:
            raise TypeError('Users should have an Email')

        if username is None:
            username = self.generate_username(full_name)

        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, full_name, email, username=None, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        if username is None:
            username = self.generate_username(full_name)

        user = self.create_user(full_name, email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def generate_username(self, full_name):
        base_username = full_name.split(' ')[0].lower()
        random_number = str(random.randint(10000, 99999))
        return base_username + random_number



AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("prefer_not_to_say", "Prefer not to say"),
)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    full_name = models.CharField(max_length=255, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    


class Avatar(models.Model):
    original = models.URLField()
    thumbnail = models.URLField()


class Address(models.Model):
    BILLING = 'billing'
    SHIPPING = 'shipping'
    ADDRESS_TYPE_CHOICES = [
        (BILLING, 'Billing'),
        (SHIPPING, 'Shipping'),
    ]

    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    default = models.BooleanField(default=False)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} Address for {self.user.full_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    avatar = models.OneToOneField(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, null=True)
    birth_date = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_products(self, *args, **kwargs):
        all_products = store.models.Product.objects.filter(realtor=self.user)
        return all_products

    def get_user_products_count(self, *args, **kwargs):
        all_products_count = store.models.Product.objects.filter(realtor=self.user).count()
        return all_products_count

    def __str__(self):  # Show name as the identifying field
        return "{}'s Profile".format(self.user.full_name)


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get("created", False):
        UserProfile.objects.get_or_create(user=kwargs.get("instance"))



class Permission(models.Model):
    name = models.CharField(max_length=255)
    guard_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='UserPermission')

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


