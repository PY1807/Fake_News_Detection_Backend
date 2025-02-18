
from .models import User,Post
from django.shortcuts import render
from .models import Signup,Post1
import datetime
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password,check_password
import json
import re
from django.core import serializers
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import time
from .utils import generate_token
from .utils import extract_mobile_number,verify_jwt,sentiment_analysis
from nltk.corpus import stopwords

def index(request):
  return render(request,'index.html')

@api_view(['GET'])
def get_all_posts(request):
    print("request aayi")
    
    token = request.headers.get('Authorization', "")

    result=verify_jwt(token)
    result = json.loads(result.content) 
    if("data" not in result.keys()):
        return JsonResponse(result)
    
    posts_cursor = Post.find({})
    
    
    posts_list = list(posts_cursor)
    
  
    formatted_posts = []
    for post in posts_list:
        not_required=['_id','text','urls','hashtags'] 
        post_data = {key: value for key, value in post.items() if key not in not_required}  # 
        formatted_posts.append(post_data)
    
    print("Output", formatted_posts)
   
    
    return JsonResponse({"posts": formatted_posts})

@api_view(['GET'])
def get_trending_posts(request):
    token = request.headers.get('Authorization', "")

    result=verify_jwt(token)
    result = json.loads(result.content) 
    if("data" not in result.keys()):
        return JsonResponse(result)
    posts = Post.find({})
    mp = {}


    for post in posts:
     for hashtag in post['hashtags']:
        mp[hashtag] = mp.get(hashtag, 0) + 1


    top_5_hashtags = [
    {"hashtag": key, "count": value}
    for key, value in sorted(mp.items(), key=lambda item: item[1], reverse=True)[:5]
]

    return JsonResponse({"trending_posts": top_5_hashtags})



@api_view(['GET'])
def getpost_from_hashtag(request):
    token = request.headers.get('Authorization', "")

    result=verify_jwt(token)
    result = json.loads(result.content) 
    if("data" not in result.keys()):
        return JsonResponse(result)
    data=json.loads(request.body)
    hashtag=data['hashtag']
    posts = Post.find({})
    store = []
    for post in posts:
        if hashtag in post['hashtags']:
            not_required=['_id','text','urls','hashtags'] 
            post_data = {key: value for key, value in post.items() if key not in not_required} 
            store.append(post_data)

    return JsonResponse({"posts": store}, safe=False)
@api_view(['POST'])
def signup_user(request):
    
    data = json.loads(request.body) 
    
    contact_no = data.get('contact_number')
    check_user=User.find_one({"contact_number":contact_no})
    if check_user:
        return JsonResponse({"status": "unsuccessful", "message": "A person with the same mobile number exists"})
    
    
    hashed_password = make_password(data.get('password'))
    
    curr = time.time()
    user = Signup(
        name=data.get('name'),
        
        email=data.get('email'),
        password=hashed_password,
        contact_number=data.get('contact_number'),
        date_joined=time.ctime(curr)
    )
    user_dict = user.to_dict()
    print("Ab aayega")
    print(user_dict)
    contact=data.get('contact_number')
    token=generate_token(contact)
   
    User.insert_one(user_dict)

   
    return JsonResponse({"status": "successful", "message": "Person registered","token":token})


@api_view(['POST'])
def create_post(request):

    data=json.loads(request.body)
    token = request.headers.get('Authorization', "")

    result=verify_jwt(token)
    result = json.loads(result.content) 
    if("data" not in result.keys()):
        return JsonResponse(result)
    mobile_number=result["data"]["mobile"]
    check_user=User.find_one({"contact_number":mobile_number})
    if not check_user:
        return JsonResponse({"status": "unsuccessful", "message": "User not found"})
    
   
    content = data.get('content', '')
    
   
    hashtags = re.findall(r'#\w+', content)   
    
    
    urls = re.findall(r'(https?://\S+|ftp://\S+|www\.\S+)', content)  
    
   
    content_cleaned = re.sub(r'#\w+', '', content)  
    content_cleaned = re.sub(r'(https?://\S+|ftp://\S+|www\.\S+)', '', content_cleaned)  # 
    
    curr =time.time()
    name=check_user['username']
    dict = {
    "title": data.get("title", ""),
    "content": data.get("content", ""),
    "urls": data.get("urls", [])
    }
    result=sentiment_analysis(content)
    # user_instance=str(user_instance)
    # print(" dnj",user_instance)
    post = Post1(
        name=name,
        title=data.get('title',''),
        content=data.get('content',''),
        text=content_cleaned.strip(), 
         result=result, # 
        hashtags=hashtags,
        urls=urls,
        created_at=time.ctime(curr)
    )
    post_dict = post.to_dict()
 
    Post.insert_one(post_dict)

    return JsonResponse({"status": "successful", "message": "Post created successfully"})
@api_view(['POST'])
def login_user(request):
    data=json.loads(request.body)
    mobile_no=data.get('contact_number')
    password=data.get('password')
    
    token=generate_token(mobile_no)
    user=User.find_one({"contact_number":mobile_no})
    if user:
        if check_password(password,user['password']):
            token=generate_token(mobile_no)
            return JsonResponse({"status": "successful", "message": "Person logged-in","token":token})
        else:
            return JsonResponse({"status": "unsuccessful", "message": "Incorrect password"})


    else:
        return JsonResponse({"status":"User does not exist",})

@api_view(['POST'])
def auth(request):

    
    
    token = request.headers.get('Authorization', "")
   
    result=verify_jwt(token)
    result = json.loads(result.content) 
    if("data" not in result.keys()):
        return JsonResponse(result)
    mobile_number=result["data"]["mobile"]
    user=User.find_one({"contact_number":mobile_number})
    
    if user:
        result["name"] = user.get("name", "")
    
    return JsonResponse(result)

@api_view(['GET'])
def search(request):

    token = request.headers.get('Authorization', "")
    result=verify_jwt(token)
    result = json.loads(result.content) 
    if("data" not in result.keys()):
        return JsonResponse(result)
    
    stop_words = set(stopwords.words('english'))
  
    
    text = request.GET.get('query', '')
    filtered_words = [word for word in text.split() if word.lower() not in stop_words]


    if not filtered_words:
     posts = []
    else:
    
     regex_queries = [{"title": {"$regex": word, "$options": "i"}} for word in filtered_words]

    
     posts = Post.find({"$or": regex_queries})
    formatted_posts = []
    for post in posts:
        post_data = {key: value for key, value in post.items() if key != '_id'}  
        formatted_posts.append(post_data)
    return JsonResponse({"posts":formatted_posts})

@api_view(['GET'])
def verify(request):
    token=request.headers.get('Authorization',"")
    result=verify_jwt(token)
    result=json.loads(result.content)
    if "data" not in result:
        return result
    data=json.loads(request.body)
    text=data["ver_text"]
    result=sentiment_analysis(text)
    return JsonResponse({"result":result})



