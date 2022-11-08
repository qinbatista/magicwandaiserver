from django.conf.urls import url
from blog import views
urlpatterns=[
    url(r'^index$',views.index),
    url(r'^login$',views.login),
    url(r'^login_check$',views.login_check)
]