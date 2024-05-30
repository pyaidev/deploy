from django.core.management import BaseCommand

from config.settings import CSU_USER_NAME, CSU_USER_PASSWORD
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            got_object = User.objects.get(email=CSU_USER_NAME)
            got_object.delete()
        except User.DoesNotExist:
            pass
        finally:

            # Create a superuser with the specified email address
            user = User.objects.create(
                email=CSU_USER_NAME,
                FIO='',  # Fill in user's full name if needed
                comment='',  # Add any additional comments about the user if needed
                phone='',  # Provide a phone number if needed
                is_staff=True,  # Grant superuser access to the admin interface
                is_superuser=True,  # Grant superuser privileges
            )

            # Set the password for the superuser
            user.set_password(CSU_USER_PASSWORD)

            # Save the superuser instance to the database
            user.save()
