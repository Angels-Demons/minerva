from django.conf.urls import url
from django.urls import path
from accounts.views import login, register


urlpatterns = [
    url(r'^register/$', register, name='register'),
    path('login/', login, name='login'),
]
