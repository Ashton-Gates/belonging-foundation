# belonging/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password 
from .models import ScholarshipApplication, VendorApplication, CustomUser, Scholarship
from django.core.mail import send_mail
admin.site.register(ScholarshipApplication)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'status')
    actions = ['approve_application']

    def approve_application(self, request, queryset):
        for application in queryset:
            if application.status != 'approved':  # Assuming you have a status field
                # Create user account
                new_user = CustomUser.objects.create(
                    username=application.user.username,
                    password=make_password('defaultpassword'),  # It's better to send a password reset link
                    email=application.user.email,
                    first_name=application.user.first_name,
                    last_name=application.user.last_name,
                )
                # Set group, permissions, etc. here
                # ...

                # Update application status
                application.status = 'approved'
                application.save()

                # Send email notification
                send_mail(
                    'Your Application is Approved',
                    'Your vendor account has been created.',
                    'from@example.com',
                    [application.user.email],
                    fail_silently=False,
                )
    approve_application.short_description = "Approve selected applications"

admin.site.register(VendorApplication, VendorApplicationAdmin)


class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Customize as needed
    # You can add search_fields, list_filter, etc. for better admin interface

admin.site.register(Scholarship, ScholarshipAdmin)

####
