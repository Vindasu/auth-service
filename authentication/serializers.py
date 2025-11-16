from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles creating new users with username, email, and password.
    Validates that username and email are unique.
    """
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long."
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Enter the same password as above for verification."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate_username(self, value):
        """Check if username is already taken."""
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate_email(self, value):
        """Check if email is valid and not already taken."""
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()  # Store emails in lowercase
    
    def validate(self, attrs):
        """Validate that both passwords match."""
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        
        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        
        # Use Django's password validators
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        return attrs
    
    def create(self, validated_data):
        """Create and return a new user."""
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Accepts either username OR email along with password.
    Returns the authenticated user if credentials are valid.
    """
    login = serializers.CharField(
        help_text="Enter your username or email address"
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Enter your password"
    )
    
    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        
        if login and password:
            # Try to authenticate with our custom backend that supports email/username
            user = authenticate(
                request=self.context.get('request'),
                username=login,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Unable to login with provided credentials.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.',
                    code='authorization'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "login" and "password".',
                code='authorization'
            )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.
    
    Used to return user information after login or for profile views.
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'is_active', 'email_verified', 
            'date_joined', 'last_login'
        )
        read_only_fields = (
            'id', 'is_active', 'email_verified', 
            'date_joined', 'last_login'
        )


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    
    Allows users to update their first name, last name, and email.
    Username cannot be changed for security reasons.
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def validate_email(self, value):
        """Check if email is valid and not already taken by another user."""
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Check if email is taken by another user (not the current user)
        if User.objects.filter(email__iexact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return value.lower()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    
    Requires current password and new password confirmation.
    """
    current_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Enter your current password"
    )
    new_password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'},
        help_text="Enter your new password (minimum 8 characters)"
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Confirm your new password"
    )
    
    def validate_current_password(self, value):
        """Check that the current password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate(self, attrs):
        """Validate that new passwords match and meet requirements."""
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        
        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm': 'New passwords do not match.'
            })
        
        # Use Django's password validators
        try:
            validate_password(new_password, user=self.context['request'].user)
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        
        return attrs
    
    def save(self, **kwargs):
        """Save the new password."""
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user