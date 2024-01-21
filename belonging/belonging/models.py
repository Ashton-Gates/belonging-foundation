from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Meta:
        # Give unique related names to avoid clashing
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email',)

    # Additional fields can be added here, if needed
