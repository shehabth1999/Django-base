from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.validators import EG_PhoneNumberValidator, AlphabeticValidator

class CustomUserManager(BaseUserManager):
    
    def create_user(self, phone_number, username, password, **extra_fields):
        if not phone_number:
            raise ValueError(_('The phone number must be set'))
        if not username:
            raise ValueError(_('The username must be set'))
        user = self.model(
            phone_number=phone_number,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)  
        return user

    def create_superuser(self, phone_number, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, username, password, **extra_fields)

class CustomUser(AbstractUser):

    first_name = models.CharField(_("first name"), max_length=150, blank=True, validators=[AlphabeticValidator(),])
    last_name = models.CharField(_("last name"), max_length=150, blank=True, validators=[AlphabeticValidator(),])
    email = None    
    phone_number = models.CharField(
        _('phone number'),
        max_length=11, unique=True,
        validators=[EG_PhoneNumberValidator(),],
        help_text=_('Required. 11 digits long starting with 01.'),
    )
    is_admin = models.BooleanField(_('admin'), default=False)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username