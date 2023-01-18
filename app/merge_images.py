import os
import glob
import shutil

from variables import WORKING_DIR, OUTPUT_CBZ_DIR
from pathlib import Path


def create_folders_and_files_name_dict():
    ds_store_to_rm = Path(f"{WORKING_DIR}.DS_Store")
    if ds_store_to_rm.is_file():
        os.remove(f"{WORKING_DIR}.DS_Store")

    ds_store_to_rm = Path(f"{WORKING_DIR}000/.DS_Store")
    if ds_store_to_rm.is_file():
        os.remove(f"{WORKING_DIR}000/.DS_Store")

    folders_and_files_name = {}
    for subdir, dirs, files in os.walk(WORKING_DIR):
        for file in files:
            key, value = os.path.basename(subdir), file
            folders_and_files_name.setdefault(key, []).append(f"{subdir}/{value}")

    sorted_dict = {k: folders_and_files_name[k] for k in sorted(folders_and_files_name)}

    for value_ in sorted_dict.values():
        value_.sort()

    return sorted_dict


def create_chapters_path_list(folders_and_files_name):
    return [f'{WORKING_DIR}{folder}/chapter-{folder}.png' for folder in folders_and_files_name]


def zip_chapters(chapters_path_list):
    for chapter_path in chapters_path_list:
        remove_extension = os.path.splitext(chapter_path)[0]
        take_only_number = remove_extension.rsplit('-', 3)
        print(f"Zipping JPGs folder for chapter-{take_only_number[1]}...")
        shutil.make_archive(
            f'{OUTPUT_CBZ_DIR}chapter-{take_only_number[1]}', 'zip', f'{WORKING_DIR}{take_only_number[1]}')


def change_extension_to_cbz():
    print("\n")
    print("Changing extension of the chapters from ZIP to CBZ... \n")
    for filename in glob.iglob(os.path.join(OUTPUT_CBZ_DIR, '*.zip')):
        os.rename(filename, f'{filename[:-4]}.cbz')

    print("ALL DONE, ENJOY !")


def rm_work_dir():
    dir_path = WORKING_DIR
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")


# def merge_images_in_one_png(folders_and_files_name):
#     chapters_path_list = []
#     for folder in folders_and_files_name:
#         print(f"Merging all JPGs into one PNG for chapter-{folder}...")
#         Image.MAX_IMAGE_PIXELS = None
#         images = [Image.open(x) for x in folders_and_files_name[folder]]
#         widths, heights = zip(*(i.size for i in images))
#
#         total_height = sum(heights)
#         max_width = max(widths)
#
#         new_im = Image.new('RGB', (max_width, total_height))
#
#         y_offset = 0
#         for im in images:
#             new_im.paste(im, (0, y_offset))
#             y_offset += im.size[1]
#         new_im.save(f'{WORKING_DIR}{folder}/chapter-{folder}.png')
#         chapters_path_list.append(f'{WORKING_DIR}{folder}/chapter-{folder}.png')
#
#     return chapters_path_list
#
#
# def compress_pngs(chapters_path_list):
#     for chapter_path in chapters_path_list:
#         remove_extension = os.path.splitext(chapter_path)[0]
#         take_only_number = remove_extension.rsplit('-', 3)
#         print(f"Compressing PNG for chapter-{take_only_number[1]}...")
#         Image.MAX_IMAGE_PIXELS = None
#         compressed_png = Image.open(chapter_path)
#         compressed_png = compressed_png.convert("P", palette=Image.ADAPTIVE, colors=256)
#         compressed_png.save(f'{WORKING_DIR}{take_only_number[1]}/chapter-{take_only_number[1]}.png', optimize=True)
