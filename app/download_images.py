import os
import urllib
import urllib.request

from bs4 import BeautifulSoup as BSHTML
from constants import URL
from constants import PARENT_DIR


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
    if os.path.isdir(PARENT_DIR):
        print("Chapters folder already created. Skipping... \n")
    else:
        os.mkdir(PARENT_DIR)
        print("Chapters folder created. \n")
    directories = list(range(len(chapter_numbers)))
    for directory in directories:
        try:
            path = os.path.join(PARENT_DIR, str(directory).zfill(3))
            os.mkdir(path)
        except FileExistsError:
            continue


def curl_images_from_urls(urls, full_paths):
    number_of_dirs = 0
    for base, dirs, files in os.walk(PARENT_DIR):
        for _ in dirs:
            number_of_dirs += 1
    print(f"\n")
    print(f"Number of chapter folders created: {number_of_dirs} \n")
    list_urls = list(urls)
    for path in full_paths:
        index_path = full_paths.index(path)
        print(f"### Downloading images for chapter n°{index_path}...")
        for url in list_urls:
            page = urllib.request.urlopen(url)
            soup = BSHTML(page, 'html.parser')
            images = soup.findAll('img')
            for image in list(images):
                index_path = images.index(image)
                try:
                    image['class']
                except KeyError:
                    continue
                if image['class'][0] == 'alignnone':
                    fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
                    urllib.request.urlretrieve(image['src'], fullfilename)
                    print(f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
            print("\n")
            list_urls.remove(url)
            break


def count_number_of_dirs():
    number_of_dirs = 0
    for base, dirs, files in os.walk(PARENT_DIR):
        for _ in dirs:
            number_of_dirs += 1
    list_number_of_dirs = list(range(number_of_dirs))
    full_paths = []
    for n in list_number_of_dirs:
        url = f'{PARENT_DIR}{str(n).zfill(3)}'
        full_paths.append(url)

    return full_paths
