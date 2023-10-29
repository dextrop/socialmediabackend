from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render

class CustomLoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')  # render your login page

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            oauth2_url = reverse('oauth2_provider:authorize') + "?" + request.GET.get("next").split("authorize/?")[1]
            return HttpResponseRedirect(oauth2_url)
        else:
            # Return to the login page with an error message if authentication fails
            return render(request, 'login.html', {'error': 'Invalid credentials'})
