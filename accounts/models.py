from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    """Custom User model with email as the username field and role-based permissions."""
    
    # Role choices
    ADMIN = 'admin'
    EDITOR = 'editor'
    VIEWER = 'viewer'
    
    ROLE_CHOICES = [
        (ADMIN, _('Admin')),
        (EDITOR, _('Editor')),
        (VIEWER, _('Viewer')),
    ]
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default=VIEWER)
    is_approved = models.BooleanField(_('approved'), default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_editor(self):
        return self.role == self.EDITOR or self.role == self.ADMIN
    
    @property
    def is_viewer(self):
        return True  # All users can view content
