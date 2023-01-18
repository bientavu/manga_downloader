import itertools
import os
import subprocess
from os import listdir
from os.path import isfile, join
from pathlib import Path
from pprint import pprint
import ctypes
from wand.image import Image
from wand.api import library


def create_folders_and_files_name_dict():
    path = '/Users/axel/Documents/perso/repos/manga-downloader/chapters/'

    ds_store_to_rm = Path(f"{path}.DS_Store")
    if ds_store_to_rm.is_file():
        os.remove(f"{path}.DS_Store")

    folders_and_files_name = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            key, value = os.path.basename(subdir), file
            folders_and_files_name.setdefault(key, []).append(value)

    for names in folders_and_files_name:
        folders_and_files_name[names].sort()

    return folders_and_files_name


def merge_images(folders_and_files_name):
    # Map C-API to python
    library.MagickAppendImages.argtypes = (ctypes.c_void_p, ctypes.c_bool)
    library.MagickAppendImages.restype = ctypes.c_void_p
    path = '/Users/axel/Documents/perso/repos/manga-downloader/chapters/0'
    jpg_001 = '/Users/axel/Documents/perso/repos/manga-downloader/chapters/0/001.jpg'
    jpg_002 = '/Users/axel/Documents/perso/repos/manga-downloader/chapters/0/002.jpg'

    # Append all pages into one new image
    new_ptr = library.MagickAppendImages(jpg_001, jpg_002, True)
    library.MagickWriteImage(new_ptr, b'/Users/axel/Documents/perso/repos/manga-downloader/chapters/0/output.png')
    library.DestroyMagickWand(new_ptr)


def merge_images_2(folders_and_files_name):
    path = '/Users/axel/Documents/perso/repos/manga-downloader/chapters/'
    filenames_string_creation = []
    for folder, filename in folders_and_files_name.items():
        filenames_string_creation.append(filename[0])
        pprint(filenames_string_creation)
        bash = subprocess.run(
            ["magick", "convert", "-append", "001.jpg", "002.jpg", "003.jpg", "004.jpg", "005.jpg", "chapter0.png"],
            stderr=subprocess.PIPE,
            text=True,
            cwd=path + folder)
        print(bash.stderr)
