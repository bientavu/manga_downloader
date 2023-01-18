import os
import requests

from app.selenium import retrieve_imgs_urls_with_selenium
from variables_and_constants import WORKING_DIR, URL, SELECT_MANGA, INPUTS, CLASS_SRC_NAME


def get_chapters_urls(chapter_numbers):
    chapter_numbers = chapter_numbers
    list_of_urls = []
    print("URLs that will be parsed:")
    for chapter_number in chapter_numbers:
        urls = f'{URL}{chapter_number}'
        list_of_urls.append(urls)
        print(urls)
    return list_of_urls


def requests_images(image_url, image_dl_path):
    headers = {'referer': 'https://mangas-origines.fr/'}
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
            for image in list(images_urls):
                index_path = images_urls.index(image)
                try:
                    image['class']
                except KeyError:
                    continue
                try:
                    if image['class'][0].startswith(INPUTS[SELECT_MANGA][1]) is True and len(image['class']) == 1:
                        # if image['class'][0].startswith(INPUTS[SELECT_MANGA][1]) is True or \
                        #         image['class'][1].startswith(INPUTS[SELECT_MANGA][1]) is True or \
                        #         image['class'][2].startswith(INPUTS[SELECT_MANGA][1]) is True:
                        fullfilename = os.path.join(f"{path}/", f"{str(index_path).zfill(3)}.jpg")
                        requests_images(image[CLASS_SRC_NAME].replace("\t\t\t\n\t\t\t", ""), fullfilename)
                        print(
                            f"{image['src'].rsplit('/', 1)[-1]} downloaded and renamed to {fullfilename.rsplit('/', 1)[-1]}")
                except IndexError:
                    continue
            print("\n")
            list_urls.remove(url)
            break
