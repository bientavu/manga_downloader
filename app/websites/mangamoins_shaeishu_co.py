import os
import re
import time
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
        print(f"### Downloading images for chapter n°{path[-3:]}...")
        for url in list_urls:
            images_urls = retrieve_imgs_urls_with_selenium(url)
            for chapter in CHAPTER_NUMBERS:
                manga_name = images_urls[0][2]["src"].split('/')[3].strip()
                manga_name = re.sub('[^a-zA-Z]+', '', manga_name)
                page_counter = images_urls[1][:-1]
                page_counter = page_counter[-2:]
                for page in range(1, int(page_counter)):
                    build_url = f"https://mangamoins.shaeishu.co/files/scans/{manga_name}{chapter}/{page}.png"
                    fullfilename = os.path.join(f"{path}/", f"{str(page).zfill(3)}.jpg")
                    requests_images(build_url, fullfilename)
            print("\n")
            list_urls.remove(url)
            break






#
# def curl_images_from_urls_without_selenium(urls, full_paths):
#     number_of_dirs = 0
#     for base, dirs, files in os.walk(WORKING_DIR):
#         for _ in dirs:
#             number_of_dirs += 1
#     print(f"\n")
#     print(f"Manga selected for download is: {SELECT_MANGA} \n")
#     print(f"Number of chapter folders created: {number_of_dirs} \n")
#     list_urls = list(urls)
#     for path in full_paths:
#         print(f"### Downloading images for chapter n°{path[-3:]}...")
#         for url in list_urls:
#             images_urls = retrieve_imgs_urls_with_selenium(url)
#             page_counter = images_urls[1][:-1]
#             page_counter = page_counter[-2:]
#             for image in list(images_urls):
#                 index_path = images_urls.index(image)
#                 try:
#                     image['class']
#                 except KeyError:
#                     continue
#                 try:
#                     if image['class'][0].startswith(INPUTS[SELECT_MANGA][1]) is True and len(image['class']) == 1:
#                         fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
#                         requests_images(image[CLASS_SRC_NAME].replace("\t\t\t\n\t\t\t", ""), fullfilename)
#                         print(
#                             f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
#                 except IndexError:
#                     continue
#             print("\n")
#             list_urls.remove(url)
#             break
