import os
import json
import time
import urllib
import urllib.request
import requests
import pyperclip

from bs4 import BeautifulSoup as BSHTML

from variables import URL, WORKING_DIR, CHAPTER_FROM, CHAPTER_TO, INPUTS, SELECT_MANGA, EXTENSION_DIR, WEBDRIVER_DIR, \
    EXTENSION_URL, CLASS_SRC_NAME

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_chapters_urls(chapter_numbers):
    chapter_numbers = chapter_numbers
    list_of_urls = []
    print("URLs that will be parsed:")
    for chapter_number in chapter_numbers:
        urls = f'{URL}{chapter_number}'
        list_of_urls.append(urls)
        print(urls)
    return list_of_urls


def create_folders():
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


def request_for_urls_with_cloudflare(url):
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


def request_for_images_with_cloudflare(image, fullfilename):
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


def request_for_urls_without_cloudflare(url):
    page = urllib.request.urlopen(url)
    soup = BSHTML(page, 'html.parser')
    return soup.findAll('img')


def request_for_images_without_cloudflare(image, fullfilename):
    urllib.request.urlretrieve(image['src'], fullfilename)


def request_for_urls_checks(url):
    if INPUTS[SELECT_MANGA][2] == "no_selenium":
        images_urls = request_for_urls_without_cloudflare(url)
        return images_urls
    if INPUTS[SELECT_MANGA][2] == "selenium_flaresolverr":
        images_urls = request_for_urls_with_cloudflare(url)
        return images_urls


def request_for_images_checks(image, fullfilename):
    if INPUTS[SELECT_MANGA][2] == "no_selenium":
        request_for_images_without_cloudflare(image, fullfilename)
    if INPUTS[SELECT_MANGA][2] == "selenium_flaresolverr":
        request_for_images_with_cloudflare(image, fullfilename)


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
        print(f"### Downloading images for chapter n°{path[-3:]}...")
        for url in list_urls:
            images_urls = request_for_urls_checks(url)
            for image in list(images_urls):
                index_path = images_urls.index(image)
                try:
                    image['class']
                except KeyError:
                    continue
                if image['class'][0].startswith(INPUTS[SELECT_MANGA][1]) is True:
                    # image['class'][1].startswith(INPUTS[SELECT_MANGA][1]) is True or \
                    # image['class'][2].startswith(INPUTS[SELECT_MANGA][1]) is True:
                    fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
                    request_for_images_checks(image, fullfilename)
                    print(image['src'])
                    print(f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
            print("\n")
            list_urls.remove(url)
            break


def curl_images_from_urls_with_selenium(urls, full_paths):
    number_of_dirs = 0
    for base, dirs, files in os.walk(WORKING_DIR):
        for _ in dirs:
            number_of_dirs += 1
    print(f"\n")
    print(f"Manga selected for download is: {SELECT_MANGA} \n")
    print(f"Number of chapter folders created: {number_of_dirs} \n")
    list_urls = list(urls)
    list_images_urls = []
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
                try:
                    if image['class'][0].startswith(INPUTS[SELECT_MANGA][1]) is True:
                        # image['class'][1].startswith(INPUTS[SELECT_MANGA][1]) is True or \
                        # image['class'][2].startswith(INPUTS[SELECT_MANGA][1]) is True:
                        fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
                        list_images_urls.append(image[CLASS_SRC_NAME])
                        print(f"{image[CLASS_SRC_NAME].rsplit('/', 1)[-1]} downloading...")
                except KeyError:
                    launch_selenium(path, list_images_urls)
                    print("All images downloaded")
                    list_images_urls = []
                    print("\n")
                    list_urls.remove(url)
                    break
            break


def launch_selenium(path, list_images_urls):
    chrome_options = Options()
    chrome_options.add_extension(f"{EXTENSION_DIR}extension_to_dl_via_selenium.crx")
    download_directory = {"download.default_directory": path}
    chrome_options.add_experimental_option("prefs", download_directory)
    webdriver_service = Service(f"{WEBDRIVER_DIR}chromedriver")
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    browser.get(EXTENSION_URL)
    edit_button = browser.find_element(By.ID, "editbtn")
    edit_button.click()
    pyperclip.copy("\n".join(list_images_urls))
    text_area = browser.find_element(By.ID, "txtin")
    text_area.send_keys(Keys.COMMAND, 'v')
    browser.find_element(By.ID, "btnDL").click()

    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(path)

        for fname in files:
            if fname.endswith('.crdownload') or fname.startswith('.com'):
                dl_wait = True

        seconds += 1
