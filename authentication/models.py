from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('L\'utilisateur doit avoir un email')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='friend_of')
    
    is_staff = models.BooleanField(default=False)  # Permet l'accès à l'admin
    is_superuser = models.BooleanField(default=False)  # Superutilisateur

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser  # Si l'utilisateur est superutilisateur, il a tous les droits

    def has_module_perms(self, app_label):
        return self.is_superuser  # Si l'utilisateur est superutilisateur, il a accès à tous les modules