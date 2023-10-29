"""socialmediabackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from backendapp.views.userview import UserView
from backendapp.views.searchfriends import UserSearchAPIView
from backendapp.views.connections import ConnectionView
from backendapp.views.post import PostView
from backendapp.views.likes import LikeView
from backendapp.views.verify import VerifyUserView
from backendapp.views.comments import CommentView
from backendapp.views.authurls import SignupView, LoginView, CustomLoginPageView, AuthCallbackView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view()),
    path('verify/', VerifyUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('oauth/login/', CustomLoginPageView.as_view()),
    path('callback/', AuthCallbackView.as_view()),
    path('user/', UserView.as_view()),
    path('search/friends/', UserSearchAPIView.as_view()),
    path('connections/', ConnectionView.as_view()),
    path('post/', PostView.as_view()),
    path('likes/', LikeView.as_view()),
    path('comment/', CommentView.as_view()),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # Include OAuth2 urls

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
