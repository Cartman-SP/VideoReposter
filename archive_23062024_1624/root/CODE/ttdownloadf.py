from tiktok_downloader import ttdownloader
from lxml import html
import requests

def get_tiktok_video_description(video_url):
    try:
        # Отправляем GET-запрос к странице видео
        response = requests.get(video_url)
        
        # Проверяем успешность запроса
        if response.status_code == 200:
            # Создаем объект ElementTree
            tree = html.fromstring(response.content)
            
            # Находим элемент с описанием видео
            description_element = tree.xpath('//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div/h1/span[1]')
            
            # Если элемент найден, возвращаем его текст
            if description_element:
                return description_element[0].text_content().strip()
            else:
                return "Описание не найдено"
        else:
            return "Ошибка при запросе страницы"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

def ttdownload(url):
    d=ttdownloader(url)
    title = url.split('/')[-2]+'.mp4'
    d[0].download(title)
    description = get_tiktok_video_description(url)
    return{'description':description, 'filename':title}
