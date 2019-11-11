from django.urls import path

from social_network_api import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('post/create/', views.PostCreateView.as_view()),
    path('post/like/<int:pk>/', views.PostLikesView.as_view()),
]
