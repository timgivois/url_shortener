from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^transform$', views.transform, name='transform'),
    url(r'^view$', views.view, name='view'),
    url(r'^.*$', views.redirect_short_url, name='index'),
]