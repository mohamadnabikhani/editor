from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup', views.Singup.as_view(), name='signup'),
    url(r'^login', views.Login.as_view() , name='login'),
    url(r'^logout', views.Logout.as_view(), name='logout'),

    ]
