from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault('role', 'admin')
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        return self.create_user(
            email,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser):
    user = "user"
    moderator = "moderator"
    admin = "admin"
    ROLE = [
        (user, 'user'),
        (moderator, 'moderator'),
        (admin, 'admin')
    ]
    first_name = models.CharField(max_length=20, default='Unknown')
    last_name = models.CharField(max_length=20, default='Unknown')
    role = models.CharField(max_length=10, default='user', choices=ROLE, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("id",)

    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'

    # также для работы модели пользователя должен быть переопределен
    # менеджер объектов
    objects = MyUserManager()

    # эта константа содержит список с полями, которые необходимо заполнить при создании пользователя A list of the
    # field names that will be prompted for when creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = []

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.role == self.admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == self.admin

    @property
    def is_user(self):
        return self.role == self.user

    @property
    def username(self):
        return self.email
