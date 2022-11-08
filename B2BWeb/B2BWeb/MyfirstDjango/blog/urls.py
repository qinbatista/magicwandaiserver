from django.conf.urls import url
from blog.views import LoginView,registerView,ActiveView
from  django.contrib.auth.decorators import login_required
from blog import views
app_name='blog'
urlpatterns=[
    # url(r'^$',views.index,name='index'),
    url(r'^jquery_datale$',views.jquery_datable,name='jquery_datale'),
    url(r'^register$',registerView.as_view(),name='register'),
    url(r'^login$',LoginView.as_view(),name='login'),
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active')
]