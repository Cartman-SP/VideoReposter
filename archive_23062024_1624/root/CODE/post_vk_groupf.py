import requests

def post_vk_group(video,title,description):
    user_access_token = "vk1.a.4jo2arx5NfjhMW4o1cUYKll7ZyuBTuOSwc7X3tnYfzIDdLup6kIEghtY1R8PPR0YutGb_Grk7tGsKWJXNxZErZLpM5canY5W0LPc7VrA8KnqE6J3G9ChpHkuZ_JmmuFuFTm9HHeLSOEr_IohMVRKHMwQJABe9DbxL7Y23Phz7wPRAJiVSqbL-m1dA8mCM3UZswby526STiDknbO3Ca_dug"
    params = {
        "access_token": user_access_token,  # Замени <USER_ID> на ID пользователя, статус которого хочешь получить
        "name": title,
        'description': description,
        "v": "5.199",
        'scopes':['video'],
        'group_id': 215238994
    }
    url = "https://api.vk.com/method/video.save?"
    response = requests.get(url, params=params)
    print(1111111111111111111111111,response)
    data = response.json()
    print(1111111111111111111111111,data)
    upload_url = data['response']['upload_url']
    video = video

    with open(video, 'rb') as video_file:
        files = {
            'video_file': video_file
        }
        response = requests.post(upload_url, files=files)
