from django.utils import timezone


def update_last_activity(user):
    """Update last activity for current user"""
    if user.is_authenticated:
        user.last_activity = timezone.now()
        user.save()
