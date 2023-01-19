import os
import re
import time
from itertools import product

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as BSHTML
from variables_and_constants import WORKING_DIR, URL, SELECT_MANGA, INPUTS, CLASS_SRC_NAME, CHAPTER_NUMBERS


def get_chapters_urls(chapter_numbers):
    chapter_numbers = chapter_numbers
    list_of_urls = []
    print("URLs that will be parsed:")
    for chapter_number in chapter_numbers:
        urls = f'{URL}{chapter_number}'
        list_of_urls.append(urls)
        print(urls)
    return list_of_urls


def retrieve_imgs_urls_with_selenium(url):
    chrome_options_uc = uc.ChromeOptions()
    driver = uc.Chrome(options=chrome_options_uc, use_subprocess=True)
    driver.get(url)
    time.sleep(4)
    driver.minimize_window()
    html = driver.page_source
    soup = BSHTML(html, 'html.parser')
    page_counter = soup.find('p', {'id': 'pagecountertitle'})
    return soup.findAll('img'), page_counter.text


def requests_images(image_url, image_dl_path):
    headers = {'referer': 'https://mangamoins.shaeishu.co/'}
    request = requests.post(image_url, headers=headers)
    open(image_dl_path, 'wb').write(request.content)


def curl_images_from_urls_without_selenium(urls, full_paths):
    number_of_dirs = 0
    for base, dirs, files in os.walk(WORKING_DIR):
        for _ in dirs:
            number_of_dirs += 1
    print(f"\n")
    print(f"Manga selected for download is: {SELECT_MANGA} \n")
    print(f"Number of chapter folders created: {number_of_dirs} \n")
    list_urls = list(urls)
    for path in full_paths:
        for url in list_urls:
            images_urls = retrieve_imgs_urls_with_selenium(url)
            for chapter in CHAPTER_NUMBERS:
                print(f"### Downloading images for chapter n°{chapter}...")
                manga_name = images_urls[0][2]["src"].split('/')[3].strip()
                manga_name = re.sub('[^a-zA-Z]+', '', manga_name)
                page_counter = images_urls[1][:-1]
                page_counter = page_counter[-2:]
                for page in [f"{page:02}" for page in range(1, int(page_counter))]:
                    build_url = f"https://mangamoins.shaeishu.co/files/scans/{manga_name}{chapter}/{page}.png"
                    fullfilename = os.path.join(f"{path}/", f"{str(page).zfill(3)}.jpg")
                    requests_images(build_url, fullfilename)
                    print(
                        f"{page}.png downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
            print("\n")
            list_urls.remove(url)
            break


# def test():
#     headers = {'referer': 'https://mangas-origines.fr/'}
#     request = requests.post(
#         'https://mangamoins.shaeishu.co/files/scans/jjk180/01.png',
#         headers=headers)
#     open('image3.jpg', 'wb').write(request.content)
