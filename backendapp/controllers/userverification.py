import pyotp
from django.conf import settings
from backendapp.controllers.sendverificationemail import send_email

class UserVerification():
    def __init__(self, user):
        self.user = user
        self.hotp = pyotp.HOTP(settings.APP_CONF["BASE32_SECRET_TOTP"])

    def generate_totp(self):
        """
        Generate A TOTP based on UserID and
        """
        return self.hotp.at(self.user.id)

    def verify_totp(self, otp):
        """
        Generate A TOTP based on UserID and
        """
        return self.hotp.verify(otp, self.user.id)

    def resend_email(self):
        """Resend Verification Email"""
        send_email(
            self.generate_totp(), self.user.email
        )