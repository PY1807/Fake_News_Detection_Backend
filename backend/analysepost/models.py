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


class Post(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    hashtags = models.JSONField(default=list)
    urls = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"
