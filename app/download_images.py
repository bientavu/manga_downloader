import os
import json
import urllib
import urllib.request
import requests

from bs4 import BeautifulSoup as BSHTML
from constants import URL, WORKING_DIR, CHAPTER_FROM, CHAPTER_TO, INPUTS, SELECT_MANGA


def get_chapters_urls(chapter_numbers):
    chapter_numbers = chapter_numbers
    list_of_urls = []
    print("URLs that will be parsed:")
    for chapter_number in chapter_numbers:
        urls = f'{URL}{chapter_number}'
        list_of_urls.append(urls)
        print(urls)
    return list_of_urls


def create_folders(chapter_numbers):
    if os.path.isdir(WORKING_DIR):
        print("Chapters folder already created. Skipping... \n")
    else:
        os.mkdir(WORKING_DIR)
        print("Chapters folder created. \n")
    directories = list(range(CHAPTER_FROM, CHAPTER_TO + 1))
    for directory in directories:
        try:
            path = os.path.join(WORKING_DIR, str(directory).zfill(3))
            os.mkdir(path)
        except FileExistsError:
            continue


def count_number_of_dirs():
    number_of_dirs = 0
    for base, dirs, files in os.walk(WORKING_DIR):
        for _ in dirs:
            number_of_dirs += 1
    list_number_of_dirs = list(range(CHAPTER_FROM, CHAPTER_TO + 1))
    full_paths = []
    for n in list_number_of_dirs:
        url = f'{WORKING_DIR}{str(n).zfill(3)}'
        full_paths.append(url)

    return full_paths


# def curl_images_from_urls(urls, full_paths):
#     number_of_dirs = 0
#     for base, dirs, files in os.walk(WORKING_DIR):
#         for _ in dirs:
#             number_of_dirs += 1
#     print(f"\n")
#     print(f"Number of chapter folders created: {number_of_dirs} \n")
#     list_urls = list(urls)
#     for path in full_paths:
#         print(f"### Downloading images for chapter n°{path[-3:]}...")
#         for url in list_urls:
#             page = urllib.request.urlopen(url)
#             soup = BSHTML(page, 'html.parser')
#             images = soup.findAll('img')
#             for image in list(images):
#                 index_path = images.index(image)
#                 try:
#                     image['class']
#                 except KeyError:
#                     continue
#                 if image['class'][0] == 'alignnone':
#                     fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
#                     urllib.request.urlretrieve(image['src'], fullfilename)
#                     print(
#                         f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
#             print("\n")
#             list_urls.remove(url)
#             break


def request_for_urls_with_cloudfare(url):
    json_data = {
        'cmd': 'request.get',
        'url': url,
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW...',
        'maxTimeout': 60000,
    }
    response = requests.post('http://localhost:8191/v1', json=json_data)
    json_content_response = json.loads(response.content.decode('utf-8'))
    soup = BSHTML(json_content_response['solution']['response'], 'html.parser')
    return soup.findAll('img')


def request_for_images_with_cloudfare(image, fullfilename):
    json_data_image_request = {
        'cmd': 'request.get',
        'url': f"{image['src'][1:]}",
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW...',
    }
    image_request = requests.post('http://localhost:8191/v1', json=json_data_image_request)
    if image_request.status_code == 200:
        with open(fullfilename, 'wb') as f:
            for chunk in image_request:
                f.write(chunk)


def request_for_urls_without_cloudfare(url):
    page = urllib.request.urlopen(url)
    soup = BSHTML(page, 'html.parser')
    return soup.findAll('img')


def request_for_images_without_cloudfare(image, fullfilename):
    urllib.request.urlretrieve(image['src'], fullfilename)


def request_for_urls_checks(url):
    if INPUTS[SELECT_MANGA][2] == "No":
        images_urls = request_for_urls_without_cloudfare(url)
        return images_urls
    if INPUTS[SELECT_MANGA][2] == "Yes":
        images_urls = request_for_urls_with_cloudfare(url)
        return images_urls


def request_for_images_checks(image, fullfilename):
    if INPUTS[SELECT_MANGA][2] == "No":
        request_for_images_without_cloudfare(image, fullfilename)
    if INPUTS[SELECT_MANGA][2] == "Yes":
        request_for_images_with_cloudfare(image, fullfilename)


def curl_images_from_urls(urls, full_paths):
    number_of_dirs = 0
    for base, dirs, files in os.walk(WORKING_DIR):
        for _ in dirs:
            number_of_dirs += 1
    print(f"\n")
    print(f"Manga selected for download is : {SELECT_MANGA} \n")
    print(f"Number of chapter folders created: {number_of_dirs} \n")
    list_urls = list(urls)
    for path in full_paths:
        print(f"### Downloading images for chapter n°{path[-3:]}...")
        for url in list_urls:
            images_urls = request_for_urls_checks(url)
            for image in list(images_urls):
                index_path = images_urls.index(image)
                try:
                    image['class']
                except KeyError:
                    continue
                if image['class'][0] == INPUTS[SELECT_MANGA][1]:
                    fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
                    request_for_images_checks(image, fullfilename)
                    print(
                        f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}"
                    )
            print("\n")
            list_urls.remove(url)
            break
