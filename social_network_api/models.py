from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='День Народження')


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    users_likes = models.ManyToManyField(User, related_name='likes')
