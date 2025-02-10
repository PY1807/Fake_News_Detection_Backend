from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="index"),
      path('hashtags/',views.getpost_from_hashtag,name='getpost_from_hashtag'),  # 
    path('allposts/', views.get_all_posts, name="get_all_posts"),
    path('posts/create/', views.create_post, name="create_post"), 
    path('login/',views.login_user,name="login_user"),
    path('signup/', views.signup_user, name="signup_user"), 
    path('trendingposts/',views.get_trending_posts,name="get_trending_posts")
]
