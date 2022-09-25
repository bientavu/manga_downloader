from app.download_images import get_chapters_urls, create_folders, count_number_of_dirs, curl_images_from_urls
from app.merge_images import create_folders_and_files_name_dict, zip_chapters, \
    create_chapters_path_list, change_extension_to_cbz, rm_work_dir
from constants import CHAPTER_NUMBERS


create_folders(CHAPTER_NUMBERS)
chapters_urls = get_chapters_urls(CHAPTER_NUMBERS)
full_paths = count_number_of_dirs()
curl_images_from_urls(chapters_urls, full_paths)

folders_and_files_name = create_folders_and_files_name_dict()
chapters_path_list = create_chapters_path_list(folders_and_files_name)
zip_chapters(chapters_path_list)
change_extension_to_cbz()
rm_work_dir()
