from rest_framework import viewsets
from .models import User, Post, Hashtag
from .serializers import UserSerializer, PostSerializer, HashtagSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .utils import detect_fake_news

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def check_fake_news(self, request, pk=None):
        post = self.get_object()
        response = requests.get(f'http://localhost:8000/api/posts')
        data = response.json()

        is_fake = detect_fake_news(data)

        post.is_fake = is_fake
        post.save()

        return Response({'postid': post.postid, 'is_fake': is_fake})

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
