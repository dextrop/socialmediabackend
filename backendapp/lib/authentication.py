from oauth2_provider.models import AccessToken
from backendapp.models.users import Users
from rest_framework import authentication
from rest_framework import exceptions

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        _token = request.META.get("HTTP_AUTHORIZATION")
        try:
            token = AccessToken.objects.get(token=_token.split(" ")[1])
            user = Users.objects.get(username=token.user)
            return (user, token)
        except Exception as e:
            pass
            # print("Error Getting Token", e)
        # _token = request.META.get("HTTP_TOKEN", False)
        # if _token:
        #     try:
        #         tokenobj = AccessToken.objects.filter(token=_token)
        #         if (tokenobj.count() > 0):
        #             token = tokenobj[0]
        #         else:
        #             raise exceptions.AuthenticationFailed('Invalid access token')
        #     except Exception as e:
        #         print ("Error Getting Token", e)
        #         raise exceptions.AuthenticationFailed('Invalid access token')
        #
        #
        #     user_id = token.user_id
        #     user = Users.objects.get(_id=user_id._id)
        #     return (user, token)
        # else:
        return None

    def authenticate_header(self, request):
        return ['authentication']