"""
The function send_verification_email is triggered every time a new user is created.
The function sends OTP based on Secret And UserID.
The OTP is required for
"""
from django.dispatch import receiver
from django.db.models.signals import post_save
from backendapp.models import Users
from backendapp.controllers.userverification import UserVerification
from backendapp.controllers.userverification import send_email

# Send Verification Email Signal Receiver
@receiver(post_save, sender=Users)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        recipient_email = instance.email
        otp = UserVerification(instance).generate_totp()

        response = send_email(otp, recipient_email)

        # Log response
        print(response.status_code)
        print(response.body)
