from app.download_images import get_chapters_urls, create_folders, count_number_of_dirs, curl_images_from_urls
from app.merge_images import create_folders_and_files_name_dict, merge_images
from constants import CHAPTER_NUMBERS


create_folders(CHAPTER_NUMBERS)
chapters_urls = get_chapters_urls(CHAPTER_NUMBERS)
full_paths = count_number_of_dirs()
curl_images_from_urls(chapters_urls, full_paths)

# folders_and_files_name = create_folders_and_files_name_dict()
# merge_images(folders_and_files_name)
