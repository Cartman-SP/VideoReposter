import json
from pytube import YouTube
from bs4 import BeautifulSoup
import requests
from telegram import Bot
from tiktok_downloader import ttdownloader
from lxml import html
import Data

def post_dzen(title, description, video_path):
    token = "6591283797:AAEjT8nYNTEbwLLCVZd9KuzIR60jR2bNCk4"
    channel_name = "@reposter_investcoin"
    bot = Bot(token=token)
    message = title + "\n" + description
    with open(video_path, "rb") as video_file:
        bot.send_video(chat_id=channel_name, video=video_file, caption=message)


