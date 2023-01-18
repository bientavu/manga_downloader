import os
from variables_and_constants import WORKING_DIR, CHAPTER_TO, CHAPTER_FROM, EPISODE_FROM, EPISODE_TO


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