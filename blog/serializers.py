from rest_framework import serializers
from .models import Post

from rest_framework.generics import ListAPIView ,CreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter ,OrderingFilter #We shoude put filter in INSTALLED_APPS


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


class PostCreate(CreateAPIView):

    serializer_class = PostSerializer

    def create(self ,request, *args, **kwargs):
        return super().create(request , *args, **kwargs)


class PostUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'id' #We using id here because when want update or delete post we do that using id
    serializer_class = PostSerializer

    def put(self, request , *args, **kwargs):
        respone = super().update(request , *args, **kwargs)
        if respone.satatus_code == 200:
            from django.core.cache import cache
            post = respone.data
            cache.set('post_data_{}'.format(post['id']),{
                'title' :post['title'],
                'short_description' : post['short_description'],
                'description' : post['description'],
            })
        return respone

    def delete(self, request , *args, **kwargs):
        post_id = request.data.get('id')
        respons = super().delete(request , *args, **kwargs)
        if respons.status_code == 204:
            from django.core.cache import cache
            cache.delete('post_data_{}'.format(post_id))
        return respons