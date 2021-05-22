To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

Language: python3.6
Framework: Django



DockerFile in project folder

Created table Video to save video details.


Cron job will run in every 10 seconds. Using django cron for implementation.

APIs are 
1. GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
<url>/videos

2. Get API to search the stored videos using their title and description.
<url>/videos?search=<keyword>


Added 2 api keys so that if quota is exhausted on one, it automatically uses the next available key.

Steps to setup Django Application
RUN python manage.py migrate django_cron
RUN python manage.py runcrons
RUN python manage.py runserver 
  
