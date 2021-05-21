from django.db import models

class Video(models.Model):
    video_id = models.CharField(null=False,blank=False,max_length=250)
    title = models.CharField(null=True,blank=True,max_length=400)
    description = models.CharField(null=True,blank=True,max_length=3000)
    publishedAt = models.DateTimeField()
    thumbnailsUrls = models.URLField()
    createdAt = models.DateTimeField(auto_now_add=True,null=True,blank=True,)

