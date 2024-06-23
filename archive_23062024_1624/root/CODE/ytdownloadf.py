from bs4 import BeautifulSoup
import requests
import json
from pytube import YouTube
import random
def ytdownload(url):
    # Загружаем страницу видео для извлечения информации
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем тег <script> с переменной ytInitialPlayerResponse
    script_tag = soup.find('script', text=lambda x: x and 'var ytInitialPlayerResponse' in x)

    if script_tag:
        # Получаем содержимое тега <script>
        script_content = script_tag.string
        
        # Извлекаем JSON-структуру из переменной ytInitialPlayerResponse
        start_index = script_content.find('{')
        end_index = script_content.rfind('}') + 1
        json_data = script_content[start_index:end_index]

        # Разбираем JSON-данные
        video_info = json.loads(json_data)

        # Извлекаем нужные данные
        title = video_info['videoDetails']['title']
        description = video_info['videoDetails']['shortDescription']
                                                                    
        print("Название видео:", title)
        print("Описание видео:", description)

        # Скачиваем видео с названием "video1.mp4"
        yt = YouTube(url)
        
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        filename = str(random.randint(1000000, 9999999))+".mp4"
        video.download(filename=filename)
        thumbnail = yt.thumbnail_url
        response = requests.get(thumbnail)
        with open(filename.replace('.mp4','.jpg'), "wb") as file:
            file.write(response.content)
        print("Обложка успешно сохранена как filename.jpg.")
        return {'filename':filename,'title':title,'description':description}
    else:
        print("Тег <script> с переменной ytInitialPlayerResponse не найден на странице.")

