from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),  # 
    path('allposts/', views.get_all_posts, name="get_all_posts"),
    path('posts/create/', views.create_post, name="create_post"), 
    path('signup/', views.signup_user, name="signup_user"), 
]
