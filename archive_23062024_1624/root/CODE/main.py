import ttdownloadf 
import ytdownloadf 
import post_dzenf 
import post_yshortsf 
import post_vk_groupf 
import post_instagramf 
import requests
import new_video
from bs4 import BeautifulSoup
import os
import time

def fromyt(url):
    ytinfo = ytdownloadf.ytdownload(url) # {'filename','title','description'}
    filename = ytinfo['filename']
    title = ytinfo['title']
    description = ytinfo['description']
    print(123)
    post_dzenf.post_dzen(title,description,filename) # (title, description, video_path)
    #post_vk_groupf.post_vk_group(filename,title,description) #(video_path,title,description)

def fromtt(url):
    ttinfo = ttdownloadf.ttdownload(url) # {'description', 'filename'}
    print('11111111111111111111111111111111')
    description = ttinfo['description']
    filename = ttinfo['filename']
    post_dzenf.post_dzen("",description,filename) # (title, description, video_path)
    print('2222222222222222222222222222222')
    #post_yshortsf.post_yshorts(filename,description,"") # (file_path, title, description)
    print('333333333333333333333333333333333')
    post_instagramf.post_instagram(filename,description) # (filename, name)
    print(4444444444444444444444444444444444)


def main():
    youtube_channels = ['https://www.youtube.com/UC_SzOt_1-l6eJog4sTSRCTQ']
    
    while(True):
        for channel in youtube_channels:
            yt_video = new_video.get_new_videos(channel)
            print(yt_video)
            if(yt_video):
                fromyt(yt_video)
    

        tt_video = new_video.get_tt_videos()
        if(tt_video):
            fromtt(tt_video)

        time.sleep(300)

if __name__ == "__main__":
    main()

