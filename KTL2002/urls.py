"""KTL2002 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from products.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('', HomeView, name='home'),
    path('<pk>', ProductDetailView.as_view()),
    path('add/', AddOfferView,name='addoffer'),
    path('signup/', SignUpView, name='signup'),
    path('login/', auth_views.auth_login, name='login'),
    path('logout/',LogoutView, name='logout'),
    path('search/', SearchPage, name='search_result'),
    path('manage/',ManageView, name='manage'),
    path('exchange/', ExchangeView, name='exchange'),
    path('request/', RequestView, name='request'),
    path('wishlist/', WishListView, name='wishlist')
]
