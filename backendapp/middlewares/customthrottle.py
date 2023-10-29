from rest_framework.throttling import SimpleRateThrottle


class UserAgentRateThrottle(SimpleRateThrottle):
    scope = 'user_agent'

    # Modified base function to use email address from request
    # as cache key for Throttling.
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        email_address = request.data.get('email')
        return f"{self.scope}_{ident}_{email_address}"
