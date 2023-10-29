"""
The function send_verification_email is triggered every time a new user is created.
The function sends OTP based on Secret And UserID.
The OTP is required for
"""
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from backendapp.models import *
from django.core.cache import cache
from backendapp.controllers.userverification import UserVerification
from backendapp.controllers.userverification import send_email


def create_cache_key(instance, model_name):
    return f'{model_name}_{instance.id}'

# Update Cache for table instance whenever instance is updated
@receiver(post_save, sender=Users)
@receiver(post_save, sender=Connection)
@receiver(post_save, sender=Post)
@receiver(post_save, sender=Likes)
@receiver(post_save, sender=Comments)
def update_cache(sender, instance, **kwargs):
    model_name = sender.__name__.lower()
    cache_key = create_cache_key(instance, model_name)
    cache.set(cache_key, instance)

# Remove Cache for table instance whenever instance is deleted
@receiver(post_delete, sender=Users)
@receiver(post_delete, sender=Connection)
@receiver(post_delete, sender=Post)
@receiver(post_delete, sender=Likes)
@receiver(post_delete, sender=Comments)
def invalidate_cache(sender, instance, **kwargs):
    model_name = sender.__name__.lower()
    cache_key = create_cache_key(instance, model_name)
    cache.delete(cache_key)

# Send Verification Email Signal Receiver
@receiver(post_save, sender=Users)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        recipient_email = instance.email
        otp = UserVerification(instance).generate_totp()
        try:
            response = send_email(otp, recipient_email)
        except Exception as e:
            print (e)