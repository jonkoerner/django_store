from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user_register$', views.register),
    url(r'^user_login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^newproduct$', views.newproduct),
    url(r'^shoes$', views.shoes),
    url(r'^buy$', views.buy),
    url(r'^logout$', views.logout),
    url(r'^remove$', views.remove)
]


