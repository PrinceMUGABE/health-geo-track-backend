from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, role, password=None):
        if not email:
            raise ValueError("The email address must be provided")
        if not phone_number:
            raise ValueError("The phone number must be provided")
        if not role:
            raise ValueError("The role must be provided")

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None):
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            role='admin',
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    USERNAME_FIELD = 'email'  # Change this from 'phone_number' to 'email'
    REQUIRED_FIELDS = ['phone_number']  # Change this from ['email'] to ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email  # Change this to return email instead of phone_number 
    
    