"""twofactorauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from accounts import views 

from django.contrib import admin
import debug_toolbar
urlpatterns = [
    # urls for the function based views
    # url(r'^$', views.home, name='home'),
    # url(r'^staff/$', views.staff_view, name='staff'),
    # url(r'^admin_view/$', views.admin_view, name='admin'),
    # url(r'^super_user/$', views.super_user_view, name='superuser'),
    # url(r'^not_allowed/$', views.not_allowed, name='not_allowed'),
    # url(r'^login/$', views.signin, name='login'),
    # url(r'^signup/$', views.signup, name='signup'),

    # urls for the class based views
    url(r'^$', views.home.as_view(), name='home'),
    url(r'^staff/$', views.staff_view.as_view(), name='staff'),
    url(r'^admin_view/$', views.admin_view.as_view(), name='admin'),
    url(r'^super_user/$', views.super_user.as_view(), name='superuser'),
    url(r'^normal_user/$', views.normal_user.as_view(), name='normaluser'),
    url(r'^not_allowed/$', views.not_allowed.as_view(), name='not_allowed'),
    url(r'^login/$', views.signin.as_view(), name='login'),
    url(r'^signup/$', views.signup.as_view(), name='signup'),   
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    
    # urls for third party apps
    url(r'^admin/', admin.site.urls),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
