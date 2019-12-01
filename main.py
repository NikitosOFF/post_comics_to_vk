import requests
import pathlib
import urllib3
import os
from dotenv import load_dotenv
import random
import shutil


def download_image(image_url, path_to_image):
    response = requests.get(image_url, verify=False)
    with open(path_to_image, 'wb') as file:
        file.write(response.content)


def fetch_random_xkdc_comics(directory):
    xkdc_current_comics_api_url = 'http://xkcd.com/info.0.json'
    number_of_comics = requests.get(xkdc_current_comics_api_url).json()['num']
    random_comics = random.randint(0, number_of_comics)
    xkdc_api_url = 'http://xkcd.com/{}/info.0.json'.format(random_comics)
    response_formatted = requests.get(xkdc_api_url)
    comics_response = response_formatted.json()
    comics_url = comics_response['img']
    comics_image_type = comics_url.split('.')[-1]
    comics_name = '{}.{}'.format(comics_response['safe_title'], comics_image_type)
    path_to_image = os.path.join(directory, comics_name)
    download_image(comics_url, path_to_image)
    return comics_response


def get_wall_upload_server(access_token, group_id, version):
    vk_api_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    parametres = {
        'group_id': group_id,
        'access_token': access_token,
        'v': version
    }
    response = requests.get(vk_api_url, params=parametres)
    return response.json()['response']


def upload_comics_on_server(url, path_to_image):
    with open(path_to_image, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        return response.json()


def save_comics_on_the_wall(access_token, data_from_server, version):
    vk_api_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    parametres = {
        'group_id': '189205854',
        'photo': data_from_server['photo'],
        'server': data_from_server['server'],
        'hash': data_from_server['hash'],
        'access_token': access_token,
        'v': version
    }
    response = requests.post(vk_api_url, params=parametres)
    return response.json()['response']


def post_comics_on_the_wall(access_token, version, group_id, comics_data, photos_data):
    vk_api_url = 'https://api.vk.com/method/wall.post?'
    attachments = [
        'photo{}_{}'.format(
            str([data['owner_id'] for data in photos_data][0]),
            str([data['id'] for data in photos_data][0]))
    ]
    parametres = {
        'owner_id': '-' + group_id,
        'from_group': '1',
        'message': comics_data['safe_title'] + '\n' + comics_data['alt'],
        'attachments': attachments,
        'access_token': access_token,
        'v': version
    }
    requests.post(vk_api_url, params=parametres)


if __name__ == '__main__':
    load_dotenv()
    images_directory = 'images'
    pathlib.Path(images_directory).mkdir(parents=True, exist_ok=True)
    urllib3.disable_warnings()

    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")
    vk_version = '5.103'

    comics_data = fetch_random_xkdc_comics(images_directory)
    comics_image_type = comics_data['img'].split('.')[-1]
    comics_name = '{}.{}'.format(comics_data['safe_title'], comics_image_type)
    path_to_comics = os.path.join(images_directory, comics_name)

    photos_data = save_comics_on_the_wall(
        vk_access_token, upload_comics_on_server(
            get_wall_upload_server(
                vk_access_token,
                vk_group_id,
                vk_version)['upload_url'],
            path_to_comics),
        vk_version)

    post_comics_on_the_wall(vk_access_token, vk_version, vk_group_id, comics_data, photos_data)
    shutil.rmtree(images_directory)
