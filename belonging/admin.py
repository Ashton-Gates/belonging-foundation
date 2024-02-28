# belonging/admin.py
from django import forms
from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from .utils import send_status_email
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password 


from accounts.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from donation.models import Payment, DonorAccount
from referee.models import Referee, Referral, SponsorApplication
from applicant.models import ScholarshipApplication, VendorApplication, Scholarship


CustomUser = get_user_model()


@admin.register(SponsorApplication)
class SponsorApplicationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'approved', 'email']
    actions = ['approve_application', 'deny_application']
    list_filter = ['approved']

    def approve_application(self, request, queryset):
        for application in queryset:
            application.approved = True
            # Generate a unique Referee ID
            referee_id = self.generate_referee_id()
            # Assign the Referee ID and create Referee instance
            Referee.objects.create(user=application.user, referee_id=referee_id)
            application.save()
            # Send an email notification to the applicant
            self.send_approval_email(application, referee_id)

    def deny_application(self, request, queryset):
        # This custom form should be created to collect feedback
        form = None  # Placeholder for your denial form
        if 'apply' in request.POST:
            form = DenialFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.cleaned_data['feedback']
                for application in queryset:
                    application.feedback = feedback
                    application.save()
                    # Send an email notification to the applicant
                    self.send_denial_email(application, feedback)
                self.message_user(request, "Selected applications have been denied.")
                return
        if not form:
            form = DenialFeedbackForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'referee/deny_application.html', {'applications': queryset, 'form': form})

    def generate_referee_id(self):
        # Implement logic to generate a unique Referee ID
        return "UniqueID123"

    def send_approval_email(self, application, referee_id):
        # Implement email sending logic
        send_mail(
            'Your Sponsor Application is Approved',
            f'Congratulations, your application is approved. Your Referee ID is {referee_id}.',
            'from@example.com',
            [application.email],
            fail_silently=False,
        )

    def send_denial_email(self, application, feedback):
        # Implement email sending logic
        send_mail(
            'Your Sponsor Application is Denied',
            f'We are sorry to inform you that your application is denied. Feedback: {feedback}.',
            'from@example.com',
            [application.email],
            fail_silently=False,
        )

    approve_application.short_description = "Approve selected applications and assign Referee ID"
    deny_application.short_description = "Deny selected applications with feedback"



@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['nominee_name', 'nominee_email', 'scholarship', 'referee', 'justification']
    search_fields = ['nominee_name', 'referee__user__username']
    list_filter = ['scholarship']

# Check if the CustomUser model is already registered, if so, unregister it
if admin.site.is_registered(CustomUser):
    admin.site.unregister(CustomUser)


@admin.register(Referee)
class RefereeAdmin(admin.ModelAdmin):
    list_display = ['user', 'referee_id']
    # If you have additional fields, you can add them here

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If you need to filter the queryset for specific conditions, you can modify it here
        return qs

class DenialFeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea, required=False)

    def deny_selected_applications(modeladmin, request, queryset):
        if 'apply' in request.POST:
            # The form was submitted
            form = DenialFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.cleaned_data['feedback']
                queryset.update(status='denied', denial_feedback=feedback)
                # Send denial email here, including the feedback
                for application in queryset:
                    send_status_email(application, feedback=feedback)
                modeladmin.message_user(request, "Selected applications have been denied.")
                return HttpResponseRedirect(request.get_full_path())

        else:
            # Display the form
            form = DenialFeedbackForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'admin/deny_application.html', {'applications': queryset, 'form': form})

    deny_selected_applications.short_description = "Deny selected applications with feedback"

# Class to edit the individual scholarships that applicants will be appling for
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'deadline')
    # Add 'deadline' to the fields you want to be able to edit in the admin
    fieldsets = (
        (None, {'fields': ('title', 'description', 'deadline')}),
    )

admin.site.register(Scholarship, ScholarshipAdmin, )

#Class to for Scholarship Application viewing and listing for approve/deny
class ScholarshipApplicationForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)
    change_form_template = 'admin/scholarship_application_change_form.html'
    actions = ['deny_selected_applications']

    def deny_selected_applications(self, request, queryset):
        return
    class Meta:
        model = ScholarshipApplication
        fields = '__all__'  # Include all other fields from the model

# Class to define the Vendor Application viewing and listing for approve/deny
class VendorApplicationForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)

    class Meta:
        model = VendorApplication
        fields = '__all__'  # Include all other fields from the model



class VendorApplicationAdmin(admin.ModelAdmin):
    form = VendorApplicationForm
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status',)
    ordering = ('-created_at',)

    actions = ['approve_selected_applications', 'deny_selected_applications']

    def approve_selected_applications(self, request, queryset):
        queryset.update(status='approved')
        for application in queryset:
            send_status_email(application)
        self.message_user(request, "Selected applications have been approved.")

    approve_selected_applications.short_description = "Approve selected applications"

    def deny_selected_applications(self, request, queryset):
        queryset.update(status='denied')
        for application in queryset:
            send_status_email(application)
        self.message_user(request, "Selected applications have been denied.")

    deny_selected_applications.short_description = "Deny selected applications"

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if it's a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__is_customer=True)

admin.site.register(VendorApplication, VendorApplicationAdmin)

class ScholarshipApplicationAdmin(admin.ModelAdmin):
    form = ScholarshipApplicationForm

    list_display = ('user', 'status', 'created_at')
    list_filter = ('status',)
    ordering = ('-created_at',)

    actions = ['approve_selected_applications', 'deny_selected_applications']

    def approve_selected_applications(self, request, queryset):
        queryset.update(status='approved')
        for application in queryset:
            send_status_email(application)
        self.message_user(request, "Selected applications have been approved.")

    approve_selected_applications.short_description = "Approve selected applications"

    def deny_selected_applications(self, request, queryset):
        queryset.update(status='denied')
        for application in queryset:
            send_status_email(application)
        self.message_user(request, "Selected applications have been denied.")

    deny_selected_applications.short_description = "Deny selected applications"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)\

# Check if ScholarshipApplication is already registered, if so, unregister first
if admin.site.is_registered(ScholarshipApplication):
    admin.site.unregister(ScholarshipApplication)

# Now safely register ScholarshipApplication with its corresponding admin class
admin.site.register(ScholarshipApplication, ScholarshipApplicationAdmin)

# Admin class for DonorAccount
class DonorAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'address')
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name')
    list_filter = ('user__is_active',)

# Register the DonorAccount model with its admin class
admin.site.register(DonorAccount, DonorAccountAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'paid')
    list_filter = ('paid',)
    search_fields = ('user__username', 'description')
    date_hierarchy = 'created'  # Replace 'created' with the actual DateTime field you use to track creation time

admin.site.register(Payment, PaymentAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_customer', 'is_staff', 'is_superuser', 'is_active', 'groups')
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
