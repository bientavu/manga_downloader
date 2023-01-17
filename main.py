from app.download_images import get_chapters_urls, create_folders, count_number_of_dirs, \
    curl_images_from_urls_with_selenium, curl_images_from_urls_without_selenium, \
    get_chapters_for_custom_urls, test
from app.merge_images import create_folders_and_files_name_dict, zip_chapters, \
    create_chapters_path_list, change_extension_to_cbz, rm_work_dir
from variables_and_constants import CHAPTER_NUMBERS, INPUTS, SELECT_MANGA, SEASON_NUMBER, EPISODE_NUMBERS

create_folders()
# chapters_urls = get_chapters_for_custom_urls(CHAPTER_NUMBERS, SEASON_NUMBER, EPISODE_NUMBERS)
chapters_urls = get_chapters_urls(CHAPTER_NUMBERS)
full_paths = count_number_of_dirs()

if INPUTS[SELECT_MANGA][2] == "no_selenium":
    curl_images_from_urls_without_selenium(chapters_urls, full_paths)
if INPUTS[SELECT_MANGA][2] == "selenium_flaresolverr":
    curl_images_from_urls_with_selenium(chapters_urls, full_paths)

folders_and_files_name = create_folders_and_files_name_dict()
chapters_path_list = create_chapters_path_list(folders_and_files_name)
zip_chapters(chapters_path_list)
change_extension_to_cbz()
rm_work_dir()

# test()
