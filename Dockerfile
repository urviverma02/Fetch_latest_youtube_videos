FROM python:3.6

RUN mkdir /youtube_video_fetch
WORKDIR /youtube_video_fetch
ADD . /youtube_video_fetch/
RUN pip install -r requirements.txt

