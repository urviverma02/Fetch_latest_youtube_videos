from django.shortcuts import render
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.pagination import CursorPagination




class Pagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

class YoutubeItems(generics.ListAPIView):
    search_fields = ['title', 'description']
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter)
    filterset_fields = ['video_id']
    ordering = ('-publishedAt')
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = Pagination

