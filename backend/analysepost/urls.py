from django.urls import path
from . import views

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiI3NzU1MDAwMCIsImV4cCI6MTczOTIwMDUxMX0.PdDQXFRiw_a4YD7RIg39WDG76jtcSXatiB0vWdoAIe0

urlpatterns = [
    path('', views.index, name="index"),
      path('hashtags',views.getpost_from_hashtag,name='getpost_from_hashtag'),  # 
    path('allposts', views.get_all_posts, name="get_all_posts"),
    path('posts/create', views.create_post, name="create_post"), 
    path('login',views.login_user,name="login_user"),
    path('auth',views.auth,name="authentication"),
    path('signup', views.signup_user, name="signup_user"), 
    path('trendingposts',views.get_trending_posts,name="get_trending_posts"),
    path('search',views.search,name="search"),
    path('verify',views.verify,name="verify"),
    path('fake_posts',views.get_fake_posts,name="fake_posts")
]
