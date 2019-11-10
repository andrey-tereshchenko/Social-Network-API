from django.conf.urls import url
from social_network_api import views

urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view()),
    url(r'^post/create/$', views.PostCreateView.as_view()),
]
