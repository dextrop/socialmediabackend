from backendapp.models.users import Users
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from backendapp.middlewares.logginmixin import LoggingMixin
from backendapp.middlewares.custom_response import CustomResponse
from backendapp.controllers.userverification import UserVerification

class VerifyUserView(generics.GenericAPIView, LoggingMixin):
    allowed_methods = ("GET", "PUT", )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """
        Returns the serialized user data. The response includes
        The response includes a message, a status code, and serialized user data as payload
        """
        email = request.data.get("email")
        otp = request.data.get("email")
        if not email:
            raise ValidationError("Missing Email ID")

        if not otp:
            raise ValidationError("Missing OTP")

        try:
            user = Users.object.get(email=request.data.get("email"))
        except Exception as e:
            raise ValidationError("User for email id does not exits")

        status = UserVerification(user).verify_totp(
            otp
        )
        if status:
            setattr(user, "is_active", True)
            user.save()

        return CustomResponse(
            message="Test API",
            code=status.HTTP_201_CREATED,
            payload="User verified"
        )

