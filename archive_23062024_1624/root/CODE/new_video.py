from googleapiclient.discovery import build
import asyncio
import os
import discord
from discord.ext import commands
import Data

# Замените 'YOUR_API_KEY' на свой API-ключ
API_KEY = 'AIzaSyBVdZxl0GNtWX7rqrPwUAJL8MIT-ozFy4w'

def get_new_videos(channel_id):
    channel_id = channel_id.split('/')[-1]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='date',
        type='video',
    ).execute()
    first_line = ""
    last_video =  f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
    try:
        with open('ytlast.txt', 'r') as file:
            first_line = file.readline()
    except FileNotFoundError:
        pass
    if(first_line!=last_video):
        with open('ytlast.txt', 'w') as file:
            file.write(last_video)
        return last_video
    else:
        return False
    

async def get_last_message(channel_id, token):
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    last_message = None

    @client.event
    async def on_ready():
        print('Бот готов к работе')

        nonlocal last_message  # Используем nonlocal, чтобы изменить значение переменной в замыкании
        channel = client.get_channel(channel_id)
        if channel is None:
            print("Ошибка: Неверный ID канала или бот не имеет доступа к каналу")
            await client.close()
            return
        
        try:
            async for msg in channel.history(limit=1):
                last_message = msg.content
                print("Последнее сообщение:", last_message)
                await client.close()
                return last_message
        except discord.errors.Forbidden:
            print("Ошибка: Не хватает прав для чтения истории сообщений в этом канале")
            await client.close()

    await client.start(token)
    print('Бот завершил работу')
    return last_message

def get_tt_videos():
    last_msg = asyncio.run(get_last_message(Data.discordchannelId, Data.discordbotToken))
    last_msg = "https://www."+last_msg[1:].split(']')[0]
    print(last_msg)
    try:
        with open("ttlast.txt", "r") as file:
            if last_msg in file.read():
                return False
    except FileNotFoundError:
        pass

    with open("ttlast.txt", "a+") as file:
        file.seek(0)
        if last_msg in file.read():
            return False
        file.write(last_msg + '\n')
    return last_msg

