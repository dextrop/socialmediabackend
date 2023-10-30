from rest_framework.response import Response

from backendapp.models.users import Users
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from backendapp.middlewares.logginmixin import LoggingMixin
from backendapp.middlewares.custom_response import CustomResponse
from backendapp.controllers.userverification import UserVerification

class VerifyUserView(generics.GenericAPIView, LoggingMixin):
    allowed_methods = ("POST", )

    def post(self, request):
        """
        Returns the serialized user data. The response includes
        The response includes a message, a status code, and serialized user data as payload
        """
        email = request.data.get("email")
        otp = request.data.get("otp")
        if not email:
            raise ValidationError("Missing Email ID")

        if not otp:
            raise ValidationError("Missing OTP")

        try:
            user = Users.objects.get(email=request.data.get("email"))
        except Exception as e:
            print (e)
            raise ValidationError("User for email id does not exits")

        verificationstatus = UserVerification(user).verify_totp(
            otp
        )
        if verificationstatus:
            setattr(user, "is_active", True)
            user.save()
            print("User Verified", user)

        return CustomResponse(
            message="Verify Account API",
            code=status.HTTP_201_CREATED,
            payload="User verified"
        )

