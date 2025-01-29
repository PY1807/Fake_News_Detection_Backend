from django.db import models

class Signup(models.Model):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    contact_number = models.CharField(max_length=12)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class User(models.Model):
    userid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

class Post(models.Model):
    postid = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    hashtags = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)