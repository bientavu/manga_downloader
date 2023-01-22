import os
import time
import requests

from sys import platform
from bs4 import BeautifulSoup as BSHTML
from app.selenium import base_to_retrieve_imgs_urls_with_selenium
from variables_and_constants import WORKING_DIR, URL, SELECT_MANGA, INPUTS, CLASS_SRC_NAME


# Methods for this website:
# - Request is working and is fast
# - Selenium batch donwload not working because of cloudflare protection


##################################################
###                 Mandatory                  ###
##################################################
def get_chapters_urls(chapter_numbers):
    chapter_numbers = chapter_numbers
    list_of_urls = []
    print("URLs that will be parsed:")
    for chapter_number in chapter_numbers:
        urls = f'{URL}{chapter_number}'
        list_of_urls.append(urls)
        print(urls)
    return list_of_urls


##################################################
###                 Mandatory                  ###
##################################################
def retrieve_imgs_urls_with_selenium(url):
    driver = base_to_retrieve_imgs_urls_with_selenium(url)
    time.sleep(2)
    if platform == "darwin":
        driver.minimize_window()
    html = driver.page_source
    soup = BSHTML(html, 'html.parser')
    return soup.findAll('img')


##################################################
###            For requests method             ###
##################################################
def requests_images(image_url, image_dl_path):
    headers = {'referer': 'https://mangas-origines.fr/'}
    request = requests.post(image_url, headers=headers)
    open(image_dl_path, 'wb').write(request.content)


########################################################################
###  Downloading with requests method (only one working and is fast) ###
########################################################################
def download_images_from_urls(urls, full_paths):
    number_of_dirs = 0
    for base, dirs, files in os.walk(WORKING_DIR):
        for _ in dirs:
            number_of_dirs += 1
    print(f"\n")
    print(f"Manga selected for download is: {SELECT_MANGA} \n")
    print(f"Number of chapter folders created: {number_of_dirs} \n")
    list_urls = list(urls)
    for path in full_paths:
        print(f"### Downloading images for chapter n°{path[-3:]}...")
        for url in list_urls:
            images_urls = retrieve_imgs_urls_with_selenium(url)
            for image in list(images_urls):
                index_path = images_urls.index(image)
                try:
                    image['class']
                except KeyError:
                    continue
                try:
                    if image['class'][0].startswith(INPUTS[SELECT_MANGA][1]) is True and len(image['class']) == 1:
                        fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
                        requests_images(image[CLASS_SRC_NAME].replace("\t\t\t\n\t\t\t", ""), fullfilename)
                        print(
                            f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
                except IndexError:
                    continue
            print("\n")
            list_urls.remove(url)
            break
