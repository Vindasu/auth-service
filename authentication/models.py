from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    
    Key features:
    - Users can login with either username OR email
    - Email is required and must be unique
    - Username is also required and must be unique
    - Includes additional profile fields for future expansion
    """
    
    # Make email field required and unique
    email = models.EmailField(
        unique=True, 
        validators=[EmailValidator()],
        help_text="Required. Enter a valid email address."
    )
    
    # Username remains required (from AbstractUser) but we'll allow email login too
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    
    # Additional fields for user profile (for future features)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    # Track when user was created and last updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Email verification (for future implementation)
    email_verified = models.BooleanField(default=False)
    
    # Keep the default username field as the primary identifier
    # But we'll create a custom authentication backend to allow email login
    USERNAME_FIELD = 'username'  # This is what Django uses for login by default
    REQUIRED_FIELDS = ['email']  # Required when creating superuser
    
    class Meta:
        db_table = 'auth_user'  # Keep same table name for consistency
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user (first name)."""
        return self.first_name
    
    @property
    def is_email_verified(self):
        """Check if user's email is verified."""
        return self.email_verified
