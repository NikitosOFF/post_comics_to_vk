import requests
import pathlib
import urllib3
from os import path


def download_image(image_url, path_to_image):
    response = requests.get(image_url, verify=False)
    with open(path_to_image, 'wb') as file:
        file.write(response.content)


def fetch_xkdc_comics(directory_for_images):
    url = 'http://xkcd.com/614/info.0.json'
    response_formatted = requests.get(url)
    comics_response = response_formatted.json()
    comics_url = comics_response['img']
    comics_image_type = comics_url.split('.')[-1]
    comics_name = '{}.{}'.format(comics_response['safe_title'], comics_image_type)
    path_to_image = path.join(directory_for_images, comics_name)
    download_image(comics_url, path_to_image)
    return comics_response['alt']


if __name__ == '__main__':
    images_directory = 'images'
    pathlib.Path(images_directory).mkdir(parents=True, exist_ok=True)
    urllib3.disable_warnings()
    print(fetch_xkdc_comics(images_directory))
