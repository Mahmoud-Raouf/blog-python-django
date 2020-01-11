from rest_framework import serializers
from .models import Post

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter ,OrderingFilter


#Create PostSerializer for import fields to use with evry class [PostList , create ,delete , update]
class PostSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Post
        fields = '__all__'

class PostPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 100


class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    filter_backends = (DjangoFilterBackend ,SearchFilter ,OrderingFilter)
    filter_fields = ('id' ,)
    search_fields = ('title' ,'short_description','description' )
    ordering_fields = ['created_in'] #You can use ordering with any fields