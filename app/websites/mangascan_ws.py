import os
import time
import pyperclip
import requests
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BSHTML
from variables_and_constants import WORKING_DIR, URL, SELECT_MANGA, CHAPTER_NUMBERS, \
    EXTENSION_DIR, WEBDRIVER_DIR, EXTENSION_URL


# Methods for this website:
# - Request is working and is fast
# - Selenium not working because of cloudflare protection


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
    chrome_options_uc = uc.ChromeOptions()
    driver = uc.Chrome(options=chrome_options_uc, use_subprocess=True)
    driver.get(url)
    time.sleep(2)
    driver.minimize_window()
    html = driver.page_source
    soup = BSHTML(html, 'html.parser')
    page_counter = soup.findAll('span', {'class': 'text'})
    return soup.findAll('img'), page_counter


##################################################
###            For selenium method             ###
##################################################
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
    time.sleep(2)

    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 30:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(path)

        for fname in files:
            if fname.endswith('.crdownload') or fname.startswith('.com'):
                dl_wait = True

        seconds += 1


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
            for chapter in CHAPTER_NUMBERS:
                print(f"### Downloading images for chapter n°{chapter}...")
                manga_name = images_urls[0][2]["data-src"].split('/')[4].strip()
                page_counter = images_urls[1][-1].contents[0]
                for page in range(1, int(page_counter) + 1):
                    build_url = f"https://scansmangas.ws/scans/{manga_name}/{chapter}/{page}.jpg"
                    fullfilename = os.path.join(f"{path}/", f"{str(page).zfill(3)}.jpg")
                    requests_images(build_url, fullfilename)
                    print(f"{page}.jpg downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
                CHAPTER_NUMBERS.remove(chapter)
                break
            print("All images downloaded")
            print("\n")
            list_urls.remove(url)
            break
