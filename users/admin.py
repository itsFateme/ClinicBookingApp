# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
    )

    filter_horizontal = ('groups', 'user_permissions',)

    def save_model(self, request, obj, form, change):
        if not change:
            
            role_display_name = obj.role 
            for role_code, role_display in User.USER_ROLES:
                if role_display == role_display_name:
                    obj.role = role_code 
                    break

            obj.set_password(obj.password) 
            obj.save() 

            if obj.role in ['clinic_admin', 'system_admin', 'doctor']: 
                obj.is_staff = True
                obj.is_active = True
                obj.save(update_fields=['is_staff', 'is_active']) 


        else: 
            if 'password' in form.changed_data:
                obj.set_password(obj.password)

            if 'role' in form.changed_data:
                role_display_name = obj.role
                for role_code, role_display in User.USER_ROLES:
                    if role_display == role_display_name:
                        obj.role = role_code
                        break
                # تنظیم is_staff و is_active بر اساس نقش جدید
                if obj.role in ['clinic_admin', 'system_admin', 'doctor']:
                    obj.is_staff = True
                    obj.is_active = True
                else:
                    obj.is_staff = False
                obj.save(update_fields=['role', 'is_staff', 'is_active'])

        super().save_model(request, obj, form, change) 