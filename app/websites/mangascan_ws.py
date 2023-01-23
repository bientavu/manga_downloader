import os
import time
import requests

from sys import platform
from bs4 import BeautifulSoup as BSHTML
from app.selenium import base_to_retrieve_imgs_urls_with_selenium
from variables_and_constants import WORKING_DIR, URL, SELECT_MANGA


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
    page_counter = soup.findAll('span', {'class': 'text'})
    return soup.findAll('img'), page_counter


##################################################
###            For requests method             ###
##################################################
def requests_images(image_url, image_dl_path):
    headers = {
        'referer': 'https://mangascan.ws/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 '
        }
    request = requests.post(image_url, headers=headers)
    open(image_dl_path, 'wb').write(request.content)


##################################################
###      Downloading with requests method      ###
##################################################
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
        for url in list_urls:
            images_urls = retrieve_imgs_urls_with_selenium(url)
            print(f"### Downloading images for chapter n°{path.rsplit('/', 1)[-1]}...")
            manga_name = images_urls[0][2]["data-src"].split('/')[4].strip()
            page_counter = images_urls[1][-1].contents[0]
            for page in range(1, int(page_counter) + 1):
                build_url = f"https://scansmangas.ws/scans/{manga_name}/{path.rsplit('/', 1)[-1]}/{page}.jpg"
                fullfilename = os.path.join(f"{path}/", f"{str(page).zfill(3)}.jpg")
                requests_images(build_url, fullfilename)
                print(f"{page}.jpg downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
            print("All images downloaded")
            print("\n")
            list_urls.remove(url)
            break
