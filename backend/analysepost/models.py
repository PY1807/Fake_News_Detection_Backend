from django.db import models
from .database import db

User=db['User']
Post=db['Post']


class Signup(models.Model):
    username = models.CharField(max_length=150, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    contact_number = models.CharField(max_length=12)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    def to_dict(obj):
       
        obj_dict = obj.__dict__.copy()
        obj_dict.pop('_state', None) 
        obj_dict.pop('id', None)    
    
        return obj_dict
    
    
    
    


class Post1(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, related_name="posts")
    username=models.CharField(max_length=50)
    content = models.TextField()
    hashtags = models.JSONField(default=list)
    urls = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"
    def to_dict(obj):
       
        obj_dict = obj.__dict__.copy()
        obj_dict.pop('_state', None) 
        obj_dict.pop('id', None)    
    
        return obj_dict
