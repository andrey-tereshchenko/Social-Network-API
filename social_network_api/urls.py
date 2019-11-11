from django.urls import path

from social_network_api import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('post/create/', views.PostCreateView.as_view(), name='create_post'),
    path('post/like/<int:pk>/', views.PostLikesView.as_view()),
]
