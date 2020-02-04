from django.conf.urls import url
from django.urls import path
from accounts.views import RegisterView, login


urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='reg'),
    path('login/', login, name='login'),
]
