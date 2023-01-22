import importlib
from app.folders_creation_and_count import create_folders, count_number_of_dirs
from app.merge_images import create_folders_and_files_name_dict, zip_chapters, \
    create_chapters_path_list, change_extension_to_cbz, rm_work_dir
from variables_and_constants import INPUTS, SELECT_MANGA, CHAPTER_NUMBERS, EPISODE_NUMBERS, SEASON_NUMBER

website_modules = importlib.import_module(f"app.websites.{INPUTS[SELECT_MANGA][2]}")


def main():
    create_folders()
    chapters_urls = website_modules.get_chapters_urls(CHAPTER_NUMBERS)
    full_paths = count_number_of_dirs()
    website_modules.download_images_from_urls(chapters_urls, full_paths)

    folders_and_files_name = create_folders_and_files_name_dict()
    chapters_path_list = create_chapters_path_list(folders_and_files_name)
    zip_chapters(chapters_path_list)
    change_extension_to_cbz()
    rm_work_dir()


if __name__ == '__main__':
    main()
