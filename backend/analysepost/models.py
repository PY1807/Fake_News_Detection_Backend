from django.db import models
from .database import db

User=db['User']
Post=db['Post']


class Signup(models.Model):
    name = models.CharField(max_length=16, unique=True)
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
    
    name=models.CharField(max_length=16)
    title=models.CharField(max_length=20)
    content = models.TextField()
    text = models.TextField()
    hashtags = models.JSONField(default=list)
    urls = models.JSONField(default=list) 
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"
    def to_dict(obj):
       
        obj_dict = obj.__dict__.copy()
        obj_dict.pop('_state', None) 
        obj_dict.pop('id', None)    
    
        return obj_dict
