from django.shortcuts import render
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.pagination import CursorPagination
import os
from youtube_video_fetch import settings
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from apiclient.discovery import build
import apiclient




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


class FetchYouTube(CronJobBase):

    schedule = Schedule(run_every_mins=1) 
    code = 'youtube_api.FetchYouTube'
    def do(self):
        apiKeys = settings.YOUTUBE_API_KEYS
        time_now = datetime.now()
        last_request_time = time_now - timedelta(minutes=1)
        valid = False

        for apiKey in apiKeys:
            try:
                youtube = build("youtube", "v3", developerKey=apiKey)
                req = youtube.search().list( q="football", part="snippet",order="date", maxResults=50 ,publishedAfter=last_request))
                res = req.execute()
                valid = True
            except apiclient.errors.HttpError as err:
                code = err.resp.status
                if not(code == 400 or code == 403):
                    break

            if valid:
                break


        if valid:
            print("inserting")

            for item in res['items']:
                if item['id'].get('videoId') is not None:
                    print(item)
                    video_id = item['id'].get('videoId')
                    publishedAt = item['snippet']['publishedAt']
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    thumbnailsUrls = item['snippet']['thumbnails']['default']['url']
                    Video.objects.create(
                        video_id=video_id,
                        title=title,
                        description=description,
                        publishedAt=publishedAt,
                        thumbnailsUrls=thumbnailsUrls,
                    )




