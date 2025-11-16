from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Simplified User admin configuration that works with Python 3.14.
    
    This provides basic user management through the Django admin interface.
    """
    
    # Fields to display in the user list
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'is_active', 'email_verified', 'date_joined'
    )
    
    # Fields that can be searched
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Filters for the right sidebar
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 
        'email_verified', 'date_joined'
    )
    
    # Fields to display when editing/adding a user
    fields = (
        'username', 'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser',
        'email_verified', 'date_joined', 'last_login'
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')
    
    # Ordering
    ordering = ('-date_joined',)
    
    # Enable bulk actions
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        """Bulk action to activate users."""
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} users have been activated.")
    make_active.short_description = "Mark selected users as active"
    
    def make_inactive(self, request, queryset):
        """Bulk action to deactivate users."""
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} users have been deactivated.")
    make_inactive.short_description = "Mark selected users as inactive"
