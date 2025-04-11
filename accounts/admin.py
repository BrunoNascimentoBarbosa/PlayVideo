from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'role', 'is_approved', 'is_active')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_approved', 'is_staff', 'is_active')
    list_filter = ('role', 'is_approved', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_image')}),
        (_('Permissions'), {
            'fields': ('role', 'is_approved', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('date_joined',)
    
    def get_readonly_fields(self, request, obj=None):
        # If not superuser, make certain fields read-only
        readonly_fields = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly_fields.extend(['is_superuser', 'is_staff', 'user_permissions', 'groups'])
        
        return readonly_fields
