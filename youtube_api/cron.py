import os
from .models import *
from youtube_video_fetch import settings
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from apiclient.discovery import build
import apiclient


query_for_search="boating|sailing"
class FetchYouTube(CronJobBase):
    RUN_EVERY_MINS = 1 

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'FetchYouTube'    

    def do(self):
        apiKeys = settings.YOUTUBE_API_KEYS
        time_now = datetime.now()
        last_request_time = time_now - timedelta(minutes=1)
        valid = False

        for apiKey in apiKeys:
            try:
                youtube = build("youtube", "v3", developerKey=apiKey)
                req = youtube.search().list( q="football", part="snippet",order="date", maxResults=50)
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
                print(item)
                video_id = item['id']['videoId']
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




