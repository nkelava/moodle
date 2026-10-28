from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .enums import RoleChoices, StatusChoices


# Create your models here.

# ------ User manager ------

class UserManager(BaseUserManager):
    # Define a model manager for User model with no username field.
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password.
        if not email:
            raise ValueError('The given email must be set.')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_user(self, email, password=None, **extra_fields):
        # Create and save a regular User with the given email and password.
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# ------ Models ------

class User(AbstractBaseUser):
    username        = None
    email           = models.EmailField(verbose_name=_('email address'), unique=True)
    first_name      = models.CharField(verbose_name=_('first name'), max_length=50, blank=True, null=False)
    last_name       = models.CharField(verbose_name=_('last name'),max_length=50, blank=True, null=False)
    is_admin        = models.BooleanField(verbose_name=_("admin status"), default=False, null=False)
    is_active       = models.BooleanField(verbose_name=_("active"), default=True, null=False)
    is_staff        = models.BooleanField(verbose_name=_("staff status"), default=False, null=False)
    is_superuser    = models.BooleanField(verbose_name=_("superuser status"),default=False, null=False)
    date_joined     = models.DateTimeField(verbose_name=_("date joined"), auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name=_("last login"), auto_now=True)
    role            = models.CharField(max_length=32, 
                                       choices=[ (tag.name, tag.value) for tag in RoleChoices ],
                                       default=RoleChoices.STUDENT, 
                                       null=False)
    status          = models.CharField(max_length=16, 
                                       choices=[ (tag.name, tag.value) for tag in StatusChoices ],
                                       null=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects =  UserManager()
    
    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


