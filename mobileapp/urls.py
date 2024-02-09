"""
URL configuration for mobileapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from mobile.views import MobileListView,MobileDetailView,MobileDeleteView,MobileCreateView,MobileUpdateView,SingUpView,SingInView,  SignOutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',SingUpView.as_view(),name='register'),
    path('login/',SingInView.as_view(),name='signin'),
    path('logout/',SignOutView.as_view(),name='out'),
    path('mobile/all',MobileListView.as_view(),name='mobile-all'),
    path('mobile/<int:pk>',MobileDetailView.as_view(),name='mobile-detail'),
    path('mobile/<int:pk>/remove',MobileDeleteView.as_view(),name='mobile-remove'),
    path('mobile/add',MobileCreateView.as_view(),name='mobile-add'),
    path('mobile/<int:pk>/change',MobileUpdateView.as_view(),name='mobile-change'),
    path('api/',include('mobilerestframework.urls'))
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)