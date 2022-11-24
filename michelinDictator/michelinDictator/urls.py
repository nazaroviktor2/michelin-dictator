"""michelinDictator URL Configuration

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
from django.urls import path
from rest_framework.routers import SimpleRouter

<<<<<<< HEAD

from card.views import CardViewSet, AudioViewSet, home_page, card_page
=======
from card.models import home_page, card_page
from card.views import CardViewSet, AudioViewSet
>>>>>>> b526357 (back)
from users.views import RegisterUser, LoginUser, logout_user

from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()

router.register(r'api/card', CardViewSet)
router.register(r'api/audio', AudioViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("", home_page, name='home'),
    path("card/",card_page)

]
urlpatterns += router.urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
